import os
import zipfile
from abc import ABC, abstractmethod
from MascEntry import MascEntry
from Dictionary import Dictionary
from PrintUtils import print_red, print_blue, print_green
from Constants import BACKUPS_DIR, CACHE_DIR, LOGS_DIR
import hashlib
import shutil

class CMS(ABC):

    def __init__(self, path, name="no_name"):
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
            except:
                raise Exception("Fatal error. Wrong installation type. Are you sure this is a " + self.type + " website?")


    # List and stores all the plain text files
    def scan(self, path=""):
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


    # Return the number of plain text files in this Wordpress installation
    def files_count(self):
        return len(self.entry_list)


    # Search for malware signatures using OWASP Web Malware Scanner database
    def search_malware_signatures(self):

        results = []

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

            # Check for files applying yara rules
            if entry.is_plain_text():
                for rules in Dictionary.yara_rules:
                    try:
                        result = rules.match(data=file_data)
                        if result:
                            for rule in result:
                                results.append(self.add_result(entry, str(rule).replace("_", " ")))
                    except:
                        # FIXME I don't know but some rules aret nor readable for me
                        print_red("Some error applying rules")

        return results

    # Prepare a result and return it
    def add_result(self, entry, details):
        result = {
            "entry": entry,
            "details": details
        }
        return result

    # Make a complete backup of the current installation
    def make_backup(self):

        if not os.path.isdir(BACKUPS_DIR):
            os.mkdir(BACKUPS_DIR)

        # Set the destination directory with a prefix containing the type of the installation (wodpress, joomla, . . .)
        destination_dir = os.path.join(BACKUPS_DIR, self.type + "_" + self.name)

        try:
            if os.path.isdir(destination_dir):
                shutil.rmtree(destination_dir)
            shutil.copytree(self.path, destination_dir)
        except:
            return False

        return True

    # Unzip a zip file that contains a clean installation of the current website
    def unzip_clean_installation(self):

        filename = self.type + "-" + self.version;
        zip_filename = filename + ".zip"
        zip_path = CACHE_DIR + zip_filename

        zip_file = zipfile.ZipFile(zip_path, "r")
        zip_file.extractall(CACHE_DIR + filename)
        zip_file.close()

        return True

    @classmethod
    def transform_results(cls, results):

        total = []

        for result in results:
            total.append(result["entry"].path)

        return list(set(total))


    # Search for suspect files in the current installation
    # By now is only looking for filenames ending with numbers. It's not a final evidence because later we have
    # to check if this file belong to an official installation
    def search_suspect_files(self):
        results = []

        for entry in self.entry_list:
            if entry.name_ends_with_digits():
                results.append(self.add_result(entry, "suspect_file"))
                continue

            for file in Dictionary.suspect_files:
                if entry.path == file:
                    results.append(self.add_result(entry, "suspect_file"))

        return results


    # Compare the files of the current installation with a clean installation to look for suspect files
    # It returns the current installation files that doesn't appear in the official installation
    def compare_with_clean_installation(self):

        results = []
        clean_files = []

        # Scan the proper clean installation to store all the filenames
        clean_installation_path = os.path.join("cache", self.type + "-" + self.version)
        if not os.path.isdir(clean_installation_path):
            print_blue("No clean installation for " + self.type + " " + self.version)
            print_blue("Downloading a new one . . .")
            self.download_clean_installation()
            print_blue("Unzipping . . .")
            self.unzip_clean_installation()
            print_green("done")

        for dirpaths, root, filenames in os.walk(clean_installation_path):
            for filename in filenames:
                clean_file = os.path.join(dirpaths, filename)
                clean_file = clean_file.replace(clean_installation_path + os.sep, "")
                clean_files.append(clean_file)

        # Search for malware and suspect file to compare with a clean installation
        print_blue("Searching for malware . . .")
        results_malware = self.search_malware_signatures()
        # To avoid repeated values
        results_malware = CMS.transform_results(results_malware)

        print_blue("Searching for suspect files . . .")
        results_suspect_files = self.search_suspect_files()
        results_suspect_files = CMS.transform_results(results_suspect_files)

        total_suspected_files = results_malware + results_suspect_files
        total_suspected_files = list(set(total_suspected_files))

        print_blue("Comparing with a clean installation . . .")
        for result in total_suspected_files:
            result = result.replace(self.path + os.sep, "")
            if not result in clean_files:
                results.append(result)

        return results

    def get_log_name(self):
        return self.type + "-" + self.name + "-";

    def get_logs(self):

        results = []
        logfile_list = os.scandir(LOGS_DIR)
        for logfile in logfile_list:
            if logfile.name.startswith(self.get_log_name()):
                results.append(logfile.name)

    @abstractmethod
    def cleanup_site(self):
        pass

    @abstractmethod
    def get_version(self):
        pass

    @abstractmethod
    def search_suspect_content(self):
        pass

    @abstractmethod
    def download_clean_installation(self):
        pass


