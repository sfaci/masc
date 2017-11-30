#!/usr/bin/python3

import os
import magic
from MascEntry import MascEntry
from Wordpress import Wordpress

TEST_DIR = "test/"
WORDPRESS_DIR = TEST_DIR + "wordpress/"
CWD = os.getcwd() + "/"

entry_list = []


# Scan a full dir recursively and store 'MascEntry' objects in a list
def store_dir_content(dir_path):
    scanned_dir = os.scandir(dir_path)
    for entry in scanned_dir:
        entry_stat = os.stat(entry.path)
        if entry.is_dir():
            st_type = "dir"
        else:
            st_type = "file"

        masc_entry = MascEntry(entry.name, CWD + entry.path, entry_stat.st_size, entry_stat.st_mode, entry_stat.st_atime,
                               entry_stat.st_mtime, entry_stat.st_ctime, st_type)
        entry_list.append(masc_entry)

        if entry.is_dir():
            store_dir_content(entry.path)


# Only to test store_dir_content function
#store_dir_content(WORDPRESS_DIR)
#for me in entry_list:
#    print(me.full_path)
#    print (me.is_plain_text())

wordpress = Wordpress(WORDPRESS_DIR)
wordpress.list()
for me in wordpress.entry_list:
    print(me.full_path)

print(wordpress.files_count())