#!/usr/bin/python3

import sys
import os
import argparse
from MascUtils import MascUtils

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
    if args.site_type == "wordpress":
        MascUtils.scan_website(args.site_type, args.scan)
elif args.add_file:
    if args.site_type == "wordpress":
        MascUtils.add_suspect_file(args.add_file)
elif args.add_word:
    if args.site_type == "wordpress":
        MascUtils.add_suspect_content(args.add_word)
else:
    print("No option provided. Try execute '" + sys.argv[0] + " -h' for help")