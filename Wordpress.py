import os
from MascEntry import MascEntry
# This class represents a Wordpress installation
class Wordpress:

    def __init__(self, path):
        # Path where this Wordpress is installed
        self.path = path
        # It will contain all the plain text files
        self.entry_list = []

    # List and stores all the plain text files
    def list(self, path=""):
        if path == "":
            path = self.path
        scanned_dir = os.scandir(path)
        for entry in scanned_dir:
            entry_stat = os.stat(entry.path)
            if entry.is_dir():
                st_type = "dir"
            else:
                st_type = "file"

            masc_entry = MascEntry(entry.name, os.getcwd() + entry.path, entry_stat.st_size, entry_stat.st_mode,
                                   entry_stat.st_atime,
                                   entry_stat.st_mtime, entry_stat.st_ctime, st_type)
            self.entry_list.append(masc_entry)

            # If the entry is a directory it continues listing deeper
            if entry.is_dir():
                self.list(entry.path)

    # Return the number of plain text files in this Wordpress installation
    def files_count(self):
        return len(self.entry_list)