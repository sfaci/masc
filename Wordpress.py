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
                                   entry_stat.st_atime,
                                   entry_stat.st_mtime, entry_stat.st_ctime, st_type)
            self.entry_list.append(masc_entry)

            # If the entry is a directory it continues listing deeper
            if entry.is_dir():
                self.scan(entry.path)


    # Return the number of plain text files in this Wordpress installation
    def files_count(self):
        return len(self.entry_list)


    def find_suspect_files(self, suspect_files):

        results = []

        for entry in self.entry_list:
            if entry.name_ends_with_digits():
                results.append(entry)
                continue

            for file in suspect_files:
                if entry.path == file:
                    results.append(entry)

        return results


    def find_suspect_content(self, suspect_content):

        results = {}

        for entry in self.entry_list:
            if entry.is_file() and entry.is_plain_text():
                file = open(entry.absolute_path)
                try:
                    for current_line in file:
                        for line in suspect_content:
                            if line in current_line:
                                results[entry.absolute_path] = current_line
                except:
                    print("Error reading file: " + entry.absolute_path)

        return results
