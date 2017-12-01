import os
from abc import ABC, abstractmethod
from MascEntry import MascEntry
from Dictionary import Dictionary
from PrintUtils import print_red
import hashlib

class CMS(ABC):

    def __init__(self, path):
        super().__init__()
        # Path where this Wordpress is installed
        self.path = path
        # It will contain all the plain text files
        self.entry_list = []
        #self.version = self.get_version()


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

            masc_entry = MascEntry(entry.name, entry.path, os.getcwd() + "/" + entry.path, entry_stat.st_size, entry_stat.st_mode,
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
                results.append(entry.name)

            # Check for files applying yara rules
            if entry.is_plain_text():
                for rules in Dictionary.yara_rules:
                    try:
                        result = rules.match(data=file_data)
                        if result:
                            for rule in result:
                                results.append(entry.name)
                    except:
                        # FIXME I don't know but some rules aret nor readable for me
                        print_red("Some error applying rules")

        return results

    @abstractmethod
    def get_version(self):
        pass

    @abstractmethod
    def search_suspect_files(self):
        pass

    @abstractmethod
    def search_suspect_content(self):
        pass

    @abstractmethod
    def download_clean_installation(self):
        pass

    @abstractmethod
    def compare_with_clean_installation(self):
        pass


