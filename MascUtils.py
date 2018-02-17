import shutil
import os
import datetime

from Constants import CACHE_DIR, LOGS_DIR, BACKUPS_DIR

# Some utils to perform
class MascUtils:

    # Clean masc cache: logs and clean installation downloaded from the Internet
    @staticmethod
    def clean_cache():
        shutil.rmtree(CACHE_DIR)
        shutil.rmtree(LOGS_DIR)
        os.mkdir(CACHE_DIR)
        os.mkdir(LOGS_DIR)

    # List backups. These are the local backups that users make any time they scan a website
    @staticmethod
    def list_backups():
        backups_list = os.scandir(BACKUPS_DIR)
        for backup in backups_list:
            backup_parts = backup.name.split("_")
            date_str = datetime.datetime.fromtimestamp(os.stat(backup.path).st_atime).strftime("%d-%m-%Y %H:%M")
            print("\t" + backup_parts[1] + " : " + backup_parts[0] + " installation (" + date_str + ")")
