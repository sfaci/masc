import shutil
import os
import datetime

from masc.constants import CACHE_DIR, LOGS_DIR, BACKUPS_DIR
from masc.print_utils import print_red


class MascUtils:
    """Some utils to perform"""

    @staticmethod
    def clean_cache():
        """Clean masc cache: logs and clean installation downloaded from the Internet"""
        shutil.rmtree(CACHE_DIR)
        shutil.rmtree(LOGS_DIR)
        os.mkdir(CACHE_DIR)
        os.mkdir(LOGS_DIR)

    @staticmethod
    def list_backups():
        """List backups. These are the local backups that users make any time they scan a website"""
<<<<<<< HEAD:masc/masc_utils.py
        if not os.path.isdir(BACKUPS_DIR):
            os.mkdir(BACKUPS_DIR)

        backup_count = len(os.listdir(BACKUPS_DIR))
        if backup_count == 0:
            print_red("no backups")
            return

        backups_list = os.scandir(BACKUPS_DIR)
        for backup in backups_list:
            backup_parts = backup.name.split("_")
            date_str = datetime.datetime.fromtimestamp(os.stat(backup.path).st_atime).strftime("%d-%m-%Y %H:%M")
            print("\t" + backup_parts[1] + " : " + backup_parts[0] + " installation (" + date_str + ")")
=======
        site_list = os.scandir(BACKUPS_DIR)
        for site in site_list:
            # backup_parts = backup.name.split("_")
            # date_str = datetime.datetime.fromtimestamp(os.stat(backup.path).st_atime).strftime("%d-%m-%Y %H:%M")
            # print("\t" + backup_parts[1] + " : " + backup_parts[0] + " installation (" + date_str + ")")

            site_parts = site.name.split("_")
            print("\t" + site_parts[1] + " : " + site_parts[0])
            
            backups = os.scandir(site)
            for backup in backups:
                print("\t\t  " + "Backup date: " + backup.name)
>>>>>>> Backup-handling:MascUtils.py
