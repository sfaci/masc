import os
import urllib.request
import zipfile
import fnmatch
from CMS import CMS
from Constants import CACHE_DIR
from Dictionary import Dictionary


# This class represents a Wordpress installation
class Wordpress(CMS):

    def __init__(self, path, name):
        super().__init__(path, name)

        if not os.path.isfile(os.path.join(path, "wp-config.php")):
            raise Exception("Fatal Error. This is not a WordPress installation.")

    # Search for suspect files in the current installation
    # By now is only looking for filenames ending with numbers. It's not a final evidence because later we have
    # to check if this file belong to an official installation
    def search_suspect_files(self):

        results = []

        for entry in self.entry_list:
            if entry.name_ends_with_digits():
                results.append(self.add_result(entry, "suspect_file"))
                continue

            for file in Dictionary.suspect_files:
                if entry.path == file:
                    results.append(self.add_result(entry, "suspect_file"))

        return results


    # Compare the files of the current installation with a clean installation to look for suspect files
    # It returns the current installation files that doesn't appear in the official installation
    # TODO make someting with WP themes and other unknown content (maybe search in the Internet the structure)
    def compare_with_clean_installation(self):

        results = []

        return results


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

    # Unzip a zip file that contains a clean installation of the current website
    def unzip_clean_installation(self):

        filename = "wordpress-" + self.version;
        zip_filename = filename + ".zip"
        zip_path = CACHE_DIR + zip_filename

        zip_file = zipfile.ZipFile(zip_path, "r")
        zip_file.extractall(CACHE_DIR + filename)
        zip_file.close()

        return True

    # Cleanup the site fixing permissions and removing unnecessary files with information that exposes the website to attackers
    def cleanup_site(self):

        if not self.make_backup():
            raise Exception("An error has occured while making backup. Aborting . . .")

        # Fix permissions in folder and files
        os.chmod(self.path, 0o755)
        os.chmod(os.path.join(self.path, ".htaccess"), 0o644)
        os.chmod(os.path.join(self.path, "wp-config.php"), 0o644)
        os.chmod(os.path.join(self.path, "wp-admin"), 0o755)
        os.chmod(os.path.join(self.path, "wp-content"), 0o755)
        os.chmod(os.path.join(self.path, "wp-includes"), 0o755)

        # Delete some files that show too more information about current installation
        if os.path.isfile(os.path.join(self.path, "readme.html")):
            os.remove(os.path.join(self.path, "readme.html"))

        # Search for readme and related files to hide information about current installation and its plugin
        for dirpath, dirnames, filenames in os.walk(self.path):

            # Remove readme files. They show information about plugins/themes version
            for filename in fnmatch.filter(filenames, "*.txt"):
                os.remove(os.path.join(dirpath, filename))

            # Remove LICENSE files
            for filename in fnmatch.filter(filenames, "LICENSE"):
                os.remove(os.path.join(dirpath, filename))

            # Remove 'generator' metatag in theme files
            for filename in fnmatch.filter(filenames, "functions.php"):

                if "wp-content/themes" in dirpath:
                    file = open(os.path.join(dirpath, filename), "a")
                    file.write("remove_action('wp_head', 'wp_generator');")
                    file.close()

            # If folder hasn't index.php file, add an extra one with no code to avoid directory listing
            if not os.path.isfile(os.path.join(dirpath, "index.php")):
                file = open(os.path.join(dirpath, "index.php"), "w")
                file.write("<?php\n// masc is protecting your site\n")
                file.close()




