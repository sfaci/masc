import os
from CMS import CMS


# This class represents a Drupal installation
class Drupal(CMS):

    def __init__(self, path, name, log=True):
        super().__init__(path, name, log)

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

    def search_suspect_content(self):
        results = []

        return results

    def cleanup_site(self):

        # Generic cleaning for every CMS
        self.delete_known_files()






