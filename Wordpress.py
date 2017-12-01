import os
import urllib.request
import zipfile
from CMS import CMS
from PrintUtils import print_red, print_debug
from Constants import CACHE_DIR
from Dictionary import Dictionary


# This class represents a Wordpress installation
class Wordpress(CMS):

    def __init__(self, path):
        super().__init__(path)


    # Search for suspect files in the current installation
    # By now is only looking for filenames ending with numbers. It's not a final evidence because later we have
    # to check if this file belong to an official installation
    def search_suspect_files(self):

        results = []

        for entry in self.entry_list:
            if entry.name_ends_with_digits():
                results.append(entry)
                continue

            for file in Dictionary.suspect_files:
                if entry.path == file:
                    results.append(entry)

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

        with open(self.path + "wp-includes/version.php") as file:
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