import os
import urllib.request
import fnmatch
import logging
import datetime
from CMS import CMS
from Constants import CACHE_DIR, LOGS_DIR


# This class represents a Wordpress installation
class Wordpress(CMS):

    def __init__(self, path, name):
        super().__init__(path, name)

        if not os.path.isfile(os.path.join(path, "wp-config.php")):
            raise Exception("Fatal Error. This is not a WordPress installation.")


    # Search for suspect content in the current installation based on the masc dictionary
    def search_suspect_content(self):

        results = []
        '''
        for entry in self.entry_list:
            if entry.is_file() and entry.is_plain_text():
                file = open(entry.absolute_path)
                try:
                    for current_line in file:
                        for line in Dictionary.suspect_content:
                            if line in current_line:
                                results[entry.absolute_path] = current_line
                except:
                    print_red("Error reading file: " + entry.absolute_path)
        '''
        return results


    # Obtain the version of the current installation
    def get_version(self):

        version_line = ""

        with open(os.path.join(self.path, "wp-includes/version.php")) as file:
            for line in file:
                if "$wp_version =" in line:
                    version_line = line.lstrip()
                    break

        slices = version_line.split("'")
        return slices[1]

    # Download a clean installation of the current website
    def download_clean_installation(self):

        url = "https://wordpress.org/wordpress-" + self.version + ".zip"
        zip_file = CACHE_DIR + "wordpress-" + self.version + ".zip"

        urllib.request.urlretrieve(url, zip_file)

        if not os.path.isfile(zip_file):
            return False

        return True


    # Cleanup the site fixing permissions and removing unnecessary files with information that exposes the website to attackers
    def cleanup_site(self):

        date = datetime.datetime.now().strftime("%Y%m%d-%H%M")
        if not os.path.isdir(LOGS_DIR):
            os.mkdir(LOGS_DIR)
        logging.basicConfig(filename=LOGS_DIR + self.type + "-" + self.name + "-" + date + ".log", level=logging.INFO)

        if not self.make_backup():
            raise Exception("An error has occured while making backup. Aborting . . .")

        # Fix permissions in folder and files
        os.chmod(self.path, 0o755)
        logging.info("Changed root path permissions to 755")
        os.chmod(os.path.join(self.path, ".htaccess"), 0o644)
        logging.info("Changed .htaccess permissions to 644")
        os.chmod(os.path.join(self.path, "wp-config.php"), 0o644)
        logging.info("Changed wp-config.php permissions to 644")
        os.chmod(os.path.join(self.path, "wp-admin"), 0o755)
        logging.info("Changed wp-admin permissions to 755")
        os.chmod(os.path.join(self.path, "wp-content"), 0o755)
        logging.info("Changed wp-content permissions to 755")
        os.chmod(os.path.join(self.path, "wp-includes"), 0o755)
        logging.info("Changed wp-includes permissions to 755")

        # Delete some files that show too more information about current installation
        if os.path.isfile(os.path.join(self.path, "readme.html")):
            os.remove(os.path.join(self.path, "readme.html"))
            logging.info("Remove " + os.path.join(self.path, "readme.html"))

        # Search for readme and related files to hide information about current installation and its plugin
        for dirpath, dirnames, filenames in os.walk(self.path):
            # Remove readme files. They show information about plugins/themes version
            for filename in fnmatch.filter(filenames, "*.txt"):
                os.remove(os.path.join(dirpath, filename))
                logging.info("Remove " + os.path.join(dirpath, filename))

            # Remove LICENSE files
            for filename in fnmatch.filter(filenames, "LICENSE"):
                os.remove(os.path.join(dirpath, filename))
                logging.info("Remove " + os.path.join(dirpath, filename))

            # Remove 'generator' metatag in theme files
            for filename in fnmatch.filter(filenames, "functions.php"):

                if "wp-content/themes" in dirpath:
                    file = open(os.path.join(dirpath, filename), "a")
                    file.write("remove_action('wp_head', 'wp_generator');")
                    file.close()
                    logging.info("Added 'remove_action(\'wp-head\', \'wp_generator\');' at the enf of " +
                                 os.path.join(dirpath, filename))

            # If folder hasn't index.php file, add an extra one with no code to avoid directory listing
            if not os.path.isfile(os.path.join(dirpath, "index.php")):
                file = open(os.path.join(dirpath, "index.php"), "w")
                file.write("<?php\n// masc is protecting your site\n")
                file.close()
                logging.info("Created and empty index.php in " + dirpath)




