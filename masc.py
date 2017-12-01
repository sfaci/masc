#!/usr/bin/python3

import sys
import os
import argparse
from Wordpress import Wordpress
from Drupal import Drupal
from Joomla import Joomla
from PrintUtils import print_green, print_blue, print_results
from Dictionary import Dictionary

CWD = os.getcwd() + "/"

parser = argparse.ArgumentParser()
parser.add_argument("--site_type", help="which type of web you want to scan:: wordpress, joomla, drupal or magento",
                    choices=["wordpress", "drupal", "joomla", "magento"])
parser.add_argument("--scan", help="Scan an installation at the given PATH", metavar="PATH")
parser.add_argument("--add_file", help="Add a suspect file to the dictionary", metavar="FILENAME")
parser.add_argument("--add_word", help="Add a suspect content to the dictionary", metavar="STRING")
args = parser.parse_args()

if len(sys.argv) == 1:
    print("No arguments provided. Execute '" + sys.argv[0] + " -h' for help")
    exit()

if args.scan:
    print_blue("Reading dictionary . . . ", "")
    Dictionary.load_suspect_files(args.site_type, args.scan)
    Dictionary.load_suspect_content(args.site_type, args.scan)
    Dictionary.load_signatures()
    print_green("done.")

    cms = None
    if args.site_type == "wordpress":
        cms = Wordpress(args.scan)
    elif args.site_type == "drupal":
        cms = Drupal(args.scan)
    elif args.site_type == "joomla":
        cms = Joomla(args.scan)

    # Scan and load some information about the website
    print_blue("Scanning web site . . . ")
    cms.scan()
    print_green("done.")

    # Search for suspect files (base on several rules like dictionary, clean installation, . . .)
    print_blue("Searching for suspect files (by name) . . . ")
    results = cms.search_suspect_files()
    print_results(results, "Suspect files were found. Listing . . .", "No suspect files were found")

    #Search for suspect content (base on dictionary)
    print_blue("Searching for suspect files (by content) . . .")
    results = cms.search_suspect_content()
    print_results(results, "Suspect content were found in some file/s. Listing . . .", "No suspect content were found")

    # Search for malware (base on OWASP WebMalwareScanner signatures database)
    print_blue("Searching for malware (by signatures) . . .")
    results = cms.search_malware_signatures()
    print_green("done.")

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