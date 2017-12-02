from CMS import CMS
import urllib
import os
from Constants import CACHE_DIR


# This class represents a Drupal installation
class Drupal(CMS):

    def __init__(self, path, name):
        super().__init__(path, name)

        if not os.path.isfile(os.path.join(path, "core/lib/Drupal.php")):
            raise Exception("Fatal Error. This is not a Drupal installation.")


    def get_version(self):
        version_line = ""

        with open(os.path.join(self.path, "core/lib/Drupal.php")) as file:
            for line in file:
                if "const VERSION =" in line:
                    version_line = line.lstrip()
                    break

        slices = version_line.split("'")
        return slices[1]

    def download_clean_installation(self):

        url = "https://ftp.drupal.org/files/projects/drupal-" + self.version + ".zip"
        zip_file = CACHE_DIR + self.type + "-" + self.version + ".zip"

        urllib.request.urlretrieve(url, zip_file)

        if not os.path.isfile(zip_file):
            return False

        return True


    def search_suspect_content(self):
        results = []

        return results


    def cleanup_site(self):
        pass