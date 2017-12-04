#!/usr/bin/python3

import sys
import os
import argparse
import datetime
import shutil

from Constants import BACKUPS_DIR, LOGS_DIR, CACHE_DIR
from Custom import Custom
from Wordpress import Wordpress
from Drupal import Drupal
from PrintUtils import print_green, print_blue, print_red, print_info, print_results
from Dictionary import Dictionary

CWD = os.getcwd() + "/"

parser = argparse.ArgumentParser()
parser.add_argument("--add-file", help="Add a suspect file to the dictionary", metavar="FILENAME")
parser.add_argument("--add-word", help="Add a suspect content to the dictionary", metavar="STRING")
parser.add_argument("--clean-cache", help="Clean masc cache (cache and logs files, NO backups)", action="store_true")
parser.add_argument("--clean-site", help="Clean up the site to hide information to attackers", action="store_true")
parser.add_argument("--list-backups", help="List local backups", action="store_true")
parser.add_argument("--make-backup", help="Create a local backup of the current installation", action="store_true")
parser.add_argument("--monitor", help="Monitor site to detect changes", action="store_true")
parser.add_argument("--name", help="Name assigned to the scanned installation", metavar="NAME")
parser.add_argument("--rollback", help="Restore a local backup", action="store_true")
parser.add_argument("--scan", help="Scan an installation at the given PATH", metavar="PATH")
parser.add_argument("--site-type", help="which type of web you want to scan:: wordpress, joomla, drupal or magento",
                    choices=["wordpress", "drupal", "custom"])

print_info()
args = parser.parse_args()

if len(sys.argv) == 1:
    print("No arguments provided. Execute '" + sys.argv[0] + " -h' for help")
    exit()

if args.clean_site and not args.name:
    print_red("No name provided. You must choose a name if you want to clean up your site")
    exit()

if args.scan and not args.make_backup and not args.rollback and not args.monitor:

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
        elif args.site_type == "custom":
            cms = Custom(args.scan, name)
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
    print_blue("Loading web site . . . ")
    cms.scan()
    print_green("done.")

    # First, it makes a complete backup of the website (user can rollback later if masc clean too agressive)
    print_blue("Making a backup  . . .")
    if not cms.make_backup():
        print_red("An error has occured while making backup. Aborting . . .")
        exit()
    print_green("done")

    # If user chosen custom website, masc only try to search. Then, exit
    if args.site_type == "custom":
        print_blue("Searching for malware . . .")
        results = cms.search_malware_signatures()
        print_results(results, "Malware were found. Listing files . . .", "Congratulations! No walware were found")
        print_green("done.")
        exit()

    # Compare malware and suspect files with clean installation files
    print_blue("Let's search for malware and suspect files. Then, let's compare results with a clean installation")
    files_to_remove = cms.compare_with_clean_installation()
    if len(files_to_remove) == 0:
        print_green("No malware/suspect files were found. Congratulations! Your website seems to be clear")

    # If the user didn't choose clean the site, masc only show that some files may be infected
    if not args.clean_site:
        if len(files_to_remove) > 0:
            print_red("Malware/suspect files were found. It will be removed if you include the option --clean-site")
            for filename in files_to_remove:
                print("\t" + os.path.join(cms.path, filename))
        exit()

    # The user chosen clean up the site
    if args.clean_site:
        try:
            if len(files_to_remove) > 0:
                print_red("Malware/suspect files were found. Removing . . .")

            # Remove malware/suspect files
            for filename in files_to_remove:
                os.remove(os.path.join(cms.path, filename))
                cms.log.info("malware/suspect file removed:" + os.path.join(cms.path, filename))
            print_green("done.")

            # Perform some cleaning up operations to hide some info about the site (at this moment only available
            # for wordpress)
            print_blue("Cleaning site . . .")
            cms.cleanup_site()
            print_green("done.")

            print_blue("Some changes can have occured. See log '" + LOGS_DIR + cms.get_log_name() +
                       "'{%date} for details")
        except Exception as e:
            print(e)

# User chose list backups
elif args.list_backups:
    backups_list = os.scandir(BACKUPS_DIR)
    print_blue("Listing local backups . . .")
    for backup in backups_list:
        backup_parts = backup.name.split("_")
        date_str = datetime.datetime.fromtimestamp(os.stat(backup.path).st_atime).strftime("%d-%m-%Y %H:%M")
        print("\t" + backup_parts[1] + " : " + backup_parts[0] + " installation (" + date_str + ")")
    print_green("done.")

# User chose make a backup
elif args.make_backup:
    if not args.scan:
        print_red("You must provide the path of your website to make a backup")
        exit()

    if not args.site_type:
        print_red("You must provide the type-site option to make a backup")
        exit

    if not args.name:
        print_red("You must provide the name of your installation to make a backup")
        exit()

    print_blue("Making backup . . .")
    website = Custom(args.scan, args.name, args.site_type)
    website.make_backup()
    print_green("done.")

# User chose restore the website with a previous backup
elif args.rollback:
    if not args.scan:
        print_red("You must provide the path of your website to rollback")
        exit()

    if not args.site_type:
        print_red("You must provide the type-site option to rollback")
        exit

    if not args.name:
        print_red("You must provide the name of your installation to rollback")
        exit()

    print_blue("Restoring backup . . .")
    website = Custom(args.scan, args.name, args.site_type)
    website.rollback_backup()
    print_green("done.")

# User chose clean masc cache (logs and cache dirs)
elif args.clean_cache:
    print_blue("Cleaning program cache . . .")
    shutil.rmtree(CACHE_DIR)
    shutil.rmtree(LOGS_DIR)
    os.mkdir(CACHE_DIR)
    os.mkdir(LOGS_DIR)
    print_green("done.")

# User chose monitor current installation
elif args.monitor:
    if not args.scan:
        print_red("You must provide the path of your website to make a backup")
        exit()

    if not args.site_type:
        print_red("You must provide the type-site option to make a backup")
        exit

    if not args.name:
        print_red("You must provide the name of your installation to make a backup")
        exit()

    print_blue("Monitoring website . . .(Press CTRL+C to terminate)")
    website = Custom(args.scan, args.name, args.site_type, False)
    website.monitor()
    print_green("Finish")

elif args.add_file:
    if not args.site_type:
        print_red("You must specify the site_type to add a new suspect file")
        Dictionary.add_suspect_file(args.site_type, args.add_file)
        print_blue("Added '" + args.add_file + "' as a suspect file to the " + args.site_type + " dictionary")
elif args.add_word:
    if not args.site_type:
        print_red("Yoy must specify the site_type to add a new suspect content")
        Dictionary.add_suspect_content(args.site_type, args.add_word)
        print_blue("Added '" + args.add_word + "' as a suspect word to the " + args.site_type + " dictionary")
else:
    print("No option provided. Try execute '" + sys.argv[0] + " -h' for help")
