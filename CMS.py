import os
from abc import ABC, abstractmethod
from MascEntry import MascEntry

class CMS(ABC):

    def __init__(self, path):
        super().__init__()
        # Path where this Wordpress is installed
        self.path = path
        # It will contain all the plain text files
        self.entry_list = []
        self.version = self.get_version()


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
    def search_malware_signatures(self):
        pass

    @abstractmethod
    def download_clean_installation(self):
        pass

    @abstractmethod
    def compare_with_clean_installation(self):
        pass


