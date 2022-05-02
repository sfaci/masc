import os
import zipfile
import hashlib
import shutil
import datetime
import logging
import time
import pyclamd
import configparser
import urllib.request
import fnmatch

from progress.bar import Bar
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
from abc import ABC, abstractmethod
from termcolor import colored
from progress.spinner import Spinner

from masc.masc_entry import MascEntry
from masc.dictionary import Dictionary
from masc.print_utils import print_red, print_blue, print_green
from masc.constants import BASE_PATH, BACKUPS_DIR, CACHE_DIR, LOGS_DIR


class CMS(ABC):
    """This class represent a generic website"""
    def __init__(self, path, name="no_name", log=True):
        super().__init__()

        self.type = type(self).__name__.lower()
        # Path where this Wordpress is installed
        self.path = path
        # Website name (to store backups)
        self.name = name
        # It will contain all the plain text files
        self.entry_list = []
        if self.type == "custom":
            self.version = "custom"
        else:
            try:
                self.version = self.get_version()
            except Exception:
                raise Exception(
                    "Fatal error. Wrong installation type. Are you sure this is a " + self.type + " website?")

        # Configure logging
        if log:
            self.set_log()
            self.log = logging.getLogger(self.name)

        # Read and create download url depending of the CMS type
        config = configparser.ConfigParser()
        config.sections()
        config.read(os.path.join(BASE_PATH, 'masc.conf'))
        if self.type != 'custom':
            self.download_url = config['download_urls'][self.type] + self.version + ".zip"

    def scan(self, path=""):
        """List and stores all the files and directories to save the website structure"""
        if path == "":
            path = self.path
        scanned_dir = os.scandir(path)
        for entry in scanned_dir:
            entry_stat = os.stat(entry.path)
            if entry.is_dir():
                st_type = "dir"
            else:
                st_type = "file"

            masc_entry = MascEntry(entry.name, entry.path, entry.path, entry_stat.st_size, entry_stat.st_mode,
                                   entry_stat.st_atime, entry_stat.st_mtime, entry_stat.st_ctime, st_type)
            self.entry_list.append(masc_entry)

            # If the entry is a directory it continues listing deeper
            if entry.is_dir():
                self.scan(entry.path)

    def files_count(self):
        """Return the number of plain text files in this WordPress installation"""
        return len(self.entry_list)

    def search_malware_signatures(self):
        """Search for malware signatures using OWASP Web Malware Scanner database"""
        results = []
        using_clamv = False

        # Check is ClamAV daemon is running to include its support to scan files
        try:
            clamav = pyclamd.ClamdAgnostic()
            using_clamv = True
            clamav_message = "Using ClamAV engine"
        except Exception:
            clamav_message = "ClamAV not found. Using only checksum and YARA rules databases"

        spinner = Spinner(colored("Scanning your website (" + clamav_message + ") ", "blue"))
        for entry in self.entry_list:
            if not entry.is_file():
                continue

            # Get the checkum of each file to compare with the signatures
            file = open(entry.path, "rb")
            file_data = file.read()
            hash = hashlib.md5()
            hash.update(file_data)
            checksum = hash.hexdigest()

            # Search each checksum in the database
            # Currently there is no results using OWASP samples
            # TODO try to get more samples
            if checksum in Dictionary.signatures_db:
                malware = str(Dictionary.signatures_db[checksum])
                results.append(self.add_result(entry, malware))
                spinner.next()

            # Check for files applying yara rules
            if entry.is_plain_text():
                for rules in Dictionary.yara_rules:
                    try:
                        result = rules.match(data=file_data)
                        if result:
                            for rule in result:
                                results.append(self.add_result(entry, str(rule).replace("_", " ")))
                    except Exception:
                        # FIXME I don't know but some rules are not readable for me
                        # I think it's because the YARA version
                        print_red("Some error applying rules")
                spinner.next()

            # Check for files using ClamAV binding
            if using_clamv:
                result = clamav.scan_file(entry.path)
                if result:
                    print(result)
                    if result[entry.path][1] != "Can't open file or directory":
                        malware = result[entry.path][1]
                        results.append(self.add_result(entry, malware))
                spinner.next()

        print()
        return results

    def add_result(self, entry, details):
        """Prepare a result and return it"""
        result = {
            "entry": entry,
            "details": details
        }
        return result

    def make_backup(self):
        """Make a complete backup of the current installation"""
        if not os.path.isdir(BACKUPS_DIR):
            os.mkdir(BACKUPS_DIR)

        # Set the destination directory with a prefix containing the type of the installation (wodpress, joomla, . . .)
        baseDir = os.path.join(BACKUPS_DIR, self.type + "_" + self.name)
        destination_dir = os.path.join(baseDir, f"{datetime.datetime.now():%Y-%m-%d %H%M%S}")
        
        try:
            # Remove previous backup
            if os.path.isdir(destination_dir):
                answer = input("A previous backups exists. Do you want to overwrite it? [y|N] ")
                if answer == '' or answer.lower() == 'n':
                    print_blue("Operation cancelled by user")
                    exit()

                shutil.rmtree(destination_dir)

            print_blue("Using " + self.name + " as backup name")
            shutil.copytree(self.path, destination_dir)
            self.log.info("backup " + self.type + "_" + self.name + " created")
            return True
        except Exception:
            return False

    def rollback_backup(self):
        """Revert any change of your website using a previous backup"""
        backup_src = os.path.join(BACKUPS_DIR, self.type + "_" + self.name)
        if not os.path.isdir(backup_src):
            print_red(
                "It does not exist a backup with the given name. Are you sure it contained a " + self.type + " installation?")
            exit()

        for dirpaths, root, filenames in os.walk(backup_src):
            for filename in filenames:
                filename = os.path.join(dirpaths, filename)
                filename_dest = filename.replace(backup_src + os.sep, "")
                path_dest = os.path.dirname(filename_dest)

                if not os.path.isdir(os.path.join(self.path, path_dest)) and path_dest != "":
                    os.mkdir(os.path.join(self.path, path_dest))
                shutil.copyfile(filename, os.path.join(self.path, filename_dest))

    def unzip_clean_installation(self):
        """Unzip a zip file that contains a clean installation of the current website"""
        filename = self.type + "-" + self.version
        zip_filename = filename + ".zip"
        zip_path = CACHE_DIR + zip_filename

        zip_file = zipfile.ZipFile(zip_path, "r")
        zip_file.extractall(CACHE_DIR + filename)
        zip_file.close()

        return True

    @classmethod
    def transform_results(cls, results):
        """Transform results structure in a filepath list non-repeated"""
        total = []

        for result in results:
            total.append(result["entry"].path)

        return list(set(total))

    # TODO The main idea is searching about known suspected files in the current CMS or website
    def search_suspect_files(self):
        """
        Search for suspect files in the current installation
        By now it's only looking for filenames ending with numbers. It's not a final evidence because later we have
        to check if this file belongs to an official installation
        :return: suspect files found
        """
        results = []

        '''
        for entry in self.entry_list:
            if entry.name_ends_with_digits():
                results.append(self.add_result(entry, "suspect_file"))
                continue

            for file in Dictionary.suspect_files:
                if entry.path == file:
                    results.append(self.add_result(entry, "suspect_file"))

        '''
        return results

    def compare_with_clean_installation(self):
        """
        Compare the files of the current installation with a clean installation to look for suspect files
        :return: the current installation files that doesn't appear in the official installation
        """
        results = []
        clean_files = []

        # Scan the proper clean installation to store all the filenames
        clean_installation_path = os.path.join(CACHE_DIR, self.type + "-" + self.version)
        if not os.path.isdir(clean_installation_path):
            print_blue("No clean installation for " + self.type + " " + self.version)
            try:
                self.download_clean_installation()
            except Exception as e:
                print_red(e)
                exit()

            print_blue("Unzipping . . .")
            self.unzip_clean_installation()
            print_green("done.")
        else:
            print_blue(
                "Clean installation found in cache for " + self.type + " " + self.version + ". It will be used to compare")

        for dirpaths, root, filenames in os.walk(clean_installation_path):
            for filename in filenames:
                clean_file = os.path.join(dirpaths, filename)
                clean_file = clean_file.replace(clean_installation_path + os.sep, "")
                clean_files.append(clean_file)

        # Search for malware and suspect file to compare with a clean installation
        results_malware = self.search_malware_signatures()
        print_green("done.")
        # To avoid repeated values
        results_malware = CMS.transform_results(results_malware)

        print_blue("Searching for suspect files . . .")
        results_suspect_files = self.search_suspect_files()
        results_suspect_files = CMS.transform_results(results_suspect_files)
        print_green("done.")

        total_suspected_files = results_malware + results_suspect_files
        total_suspected_files = list(set(total_suspected_files))

        print_blue("Comparing with a clean installation . . .")
        for result in total_suspected_files:
            result = result.replace(self.path + os.sep, "")
            if result not in clean_files:
                results.append(result)
        print_green("done.")

        return results

    def get_log_name(self):
        return self.type + "-" + self.name + "-"

    def get_logs(self):
        results = []
        logfile_list = os.scandir(LOGS_DIR)
        for logfile in logfile_list:
            if logfile.name.startswith(self.get_log_name()):
                results.append(logfile.name)

        return results

    def set_log(self):
        date = datetime.datetime.now().strftime("%Y%m%d-%H%M")
        if not os.path.isdir(LOGS_DIR):
            os.mkdir(LOGS_DIR)
        logging.basicConfig(filename=LOGS_DIR + self.type + "-" + self.name + "-" + date + ".log", level=logging.INFO)

    def on_modified(self, event):
        """Notify on the screen changes during monitoring"""
        if event.is_directory:
            print("directory " + event.event_type + " " + event.src_path)
        else:
            print("file " + event.event_type + " " + event.src_path)

    def monitor(self):
        """Monitor current installation and log any changes"""
        print("Details at: " + LOGS_DIR + self.type + "-" + self.name + "-monitor.log")
        logging.basicConfig(filename=LOGS_DIR + self.type + "-" + self.name + "-monitor.log",
                            level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
        # Monitor for changes and write details to a log
        event_handler = LoggingEventHandler()
        observer = Observer()
        observer.schedule(event_handler, self.path, recursive=True)
        observer.start()

        # Monitor for changes and trigger a event
        filesystem_event = FileSystemEventHandler()
        filesystem_event.on_modified = self.on_modified
        observer.schedule(filesystem_event, self.path, recursive=True)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()

        observer.join()

    def delete_known_files(self):
        """
        Delete known files in any website (README, LICENSE and some generic txt and html files)
        Also it creates an index.php file to silence any 'index-empty' directory
        :return:
        """
        # Search for readme and related files to hide information about current installation and its plugin
        for dirpath, dirnames, filenames in os.walk(self.path):
            # Remove readme files. They show information about plugins/themes version
            for filename in fnmatch.filter(filenames, "*.txt"):
                if filename == 'robots.txt':
                    continue

                os.remove(os.path.join(dirpath, filename))
                self.log.info("file removed:" + os.path.join(dirpath, filename))

            # Remove LICENSE files
            for filename in fnmatch.filter(filenames, "LICENSE"):
                os.remove(os.path.join(dirpath, filename))
                self.log.info("file removed:" + os.path.join(dirpath, filename))

            # If folder hasn't index.php file, add an extra one with no code to avoid directory listing
            if not os.path.isfile(os.path.join(dirpath, "index.php")):
                file = open(os.path.join(dirpath, "index.php"), "w")
                file.write("<?php\n// masc is protecting your site\n")
                file.close()
                self.log.info("file created:index.php:at:" + dirpath)

    def download_clean_installation(self):
        """Download a clean installation of the current website"""
        zip_file = CACHE_DIR + self.type + "-" + self.version + ".zip"

        if not os.path.isdir(CACHE_DIR):
            os.mkdir(CACHE_DIR)

        try:
            urllib.request.urlretrieve(self.download_url, zip_file, self.download_progress)

            if not os.path.isfile(zip_file):
                return False

            return True
        except Exception as e:
            print(e)
            raise Exception(
                'Some error has produced while downloading a clean installation. Please, check your conectivity.')

    # Progress bar to show clean installation download
    bar = None

    @staticmethod
    def download_progress(block_count, block_size, total_size):
        """Update download state using a progressbar"""
        global bar

        # First time, progress bar is instantiated
        if CMS.bar is None:
            CMS.bar = Bar(colored("Downloading a new one (it will be stored to use in advance)", "blue"),
                          fill=colored("#", "blue"), max=total_size, suffix='%(percent)d%%')

        # Calculate how much is downloaded and update progress bar during the whole process
        downloaded = block_count * block_size
        if downloaded < total_size:
            CMS.bar.next(block_size)
        else:
            CMS.bar.finish()

    @abstractmethod
    def cleanup_site(self):
        pass

    @abstractmethod
    def get_version(self):
        pass

    @abstractmethod
    def search_suspect_content(self):
        pass
