#!/usr/bin/python3

import sys
import os
import argparse
import datetime
import shutil
from Constants import BACKUPS_DIR
from Wordpress import Wordpress
from Drupal import Drupal
from Joomla import Joomla
from PrintUtils import print_green, print_blue, print_red, print_info, print_results
from Dictionary import Dictionary

CWD = os.getcwd() + "/"

parser = argparse.ArgumentParser()
parser.add_argument("--site-type", help="which type of web you want to scan:: wordpress, joomla, drupal or magento",
                    choices=["wordpress", "drupal", "joomla", "magento"])
parser.add_argument("--scan", help="Scan an installation at the given PATH", metavar="PATH")
parser.add_argument("--name", help="Name assigned to the scanned installation", metavar="NAME")
parser.add_argument("--list-backups", help="List local backups", action="store_true")
parser.add_argument("--restore-backup", help="Restore a local backup", metavar="BACKUP_NAME")
parser.add_argument("--add-file", help="Add a suspect file to the dictionary", metavar="FILENAME")
parser.add_argument("--add-word", help="Add a suspect content to the dictionary", metavar="STRING")
parser.add_argument("--clean-up", help="Clean up the site to hide information to attackers", action="store_true")

print_info()
args = parser.parse_args()

if len(sys.argv) == 1:
    print("No arguments provided. Execute '" + sys.argv[0] + " -h' for help")
    exit()

if args.clean_up and not args.name:
    print_red("No name provided. You must choose a name if you want to clean up your site")
    exit()

if args.scan:

    # Set a default or choosen name
    name = "no_name"
    if args.name:
        name = args.name

    cms = None
    try:
        if args.site_type == "wordpress":
            cms = Wordpress(args.scan, name)
        elif args.site_type == "drupal":
            cms = Drupal(args.scan, name)
        elif args.site_type == "joomla":
            cms = Joomla(args.scan, name)
    except Exception as e:
        print_red(e)
        print_blue("Exiting . . .")
        exit()

    # Load dictionaries/signatures/rules from databases
    print_blue("Loading dictionaries and signatures. . . ")
    Dictionary.load_suspect_files(args.site_type, args.scan)
    Dictionary.load_suspect_content(args.site_type, args.scan)
    Dictionary.load_signatures()
    print_green("done.")

    # Scan and load some information about the website
    print_blue("Scanning web site . . . ")
    cms.scan()
    print_green("done.")

    # Compare malware and suspect files with clean installation files
    print_blue("Let's search for malware and suspect files. Then, let's compare results with a clean installation")
    files_to_remove = cms.compare_with_clean_installation()
    if len(files_to_remove) == 0:
        print_green("No malware/suspect files were found. Congratulations! Your website seems to be clear")

    if not args.clean_up:
        if len(files_to_remove) > 0:
            print_red("Malware/suspect files were found. It will be removed if you include the option --clean-up")
            for filename in files_to_remove:
                print("\t" + os.path.join(cms.path, filename))
        exit()

    if args.clean_up:

        print_blue("Cleaning site . . .")
        try:
            for filename in files_to_remove:
                os.remove(os.path.join(cms.path, filename))

            cms.cleanup_site()
            print_green("done.")
        except Exception as e:
            print(e)

elif args.list_backups:
    backups_list = os.scandir(BACKUPS_DIR)
    print_blue("Listing local backups . . .")
    for backup in backups_list:
        backup_parts = backup.name.split("_")
        date_str = datetime.datetime.fromtimestamp(os.stat(backup.path).st_atime).strftime("%d-%m-%Y %H:%M")
        print("\t" + backup_parts[1] + " : " + backup_parts[0] + " installation (" + date_str + ")")

elif args.restore_backup:
    print_blue("Restoring backup . . .")
    backup_file = os.path.join(BACKUPS_DIR, args.site_type + "_" + args.name)
    destionation = args.scan

elif args.add_file:
    if args.site_type == "wordpress":
        Dictionary.add_suspect_file(args.add_file)
        print_blue("Added '" + args.add_file + "' as a suspect file to the dictionary")
elif args.add_word:
    if args.site_type == "wordpress":
        Dictionary.add_suspect_content(args.add_word)
        print_blue("Added '" + args.add_word + "' as a suspect word to the dictionary")
else:
    print("No option provided. Try execute '" + sys.argv[0] + " -h' for help")