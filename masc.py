#!/usr/bin/python3

import sys
import os
import argparse
import datetime
from Constants import BACKUPS_DIR
from Wordpress import Wordpress
from Drupal import Drupal
from Joomla import Joomla
from PrintUtils import print_green, print_blue, print_red, print_info
from Dictionary import Dictionary

CWD = os.getcwd() + "/"

parser = argparse.ArgumentParser()
parser.add_argument("--site-type", help="which type of web you want to scan:: wordpress, joomla, drupal or magento",
                    choices=["wordpress", "drupal", "joomla", "magento"])
parser.add_argument("--scan", help="Scan an installation at the given PATH", metavar="PATH")
parser.add_argument("--name", help="Name assigned to the scanned installation", metavar="NAME")
parser.add_argument("--list-backups", help="List local backups", action="store_true")
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
    # Dictionary.load_signatures()
    print_green("done.")

    # Scan and load some information about the website
    print_blue("Scanning web site . . . ")
    cms.scan()
    print_green("done.")

    # Search for suspect files (base on several rules like dictionary, clean installation, . . .)
    #print_blue("Searching for suspect files (by name) . . . ")
    #results = cms.search_suspect_files()
    #print_results(results, "Suspect files were found. Listing . . .", "No suspect files were found")

    #Search for suspect content (base on dictionary)
    #print_blue("Searching for suspect files (by content) . . .")
    #results = cms.search_suspect_content()
    #print_results(results, "Suspect content were found in some file/s. Listing . . .", "No suspect content were found")

    # Search for malware (base on OWASP WebMalwareScanner signatures database)
    #print_blue("Searching for malware . . .")
    #results = cms.search_malware_signatures()
    #print_results(results, "Malware were found. Listing files. . .", "No malware were found")

    if args.clean_up:
        print_blue("Cleaning site . . .")
        try:
            cms.cleanup_site()
        except Exception as e:
            print(e)

elif args.list_backups:
    backups_list = os.scandir(BACKUPS_DIR)
    print_blue("Listing local backups . . .")
    for backup in backups_list:
        backup_parts = backup.name.split("_")
        date_str = datetime.datetime.fromtimestamp(os.stat(backup.path).st_atime).strftime("%d-%m-%Y %H:%M")
        print("\t" + backup_parts[1] + " : " + backup_parts[0] + " installation (" + date_str + ")")

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