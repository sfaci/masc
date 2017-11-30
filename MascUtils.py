from Wordpress import Wordpress
from Dictionary import Dictionary

# Path where clean installations are stored to check with working installations
TEST_PATH = "test/"

# Class with some static methods to perform generic operations
class MascUtils:

    # TODO compare a working installation with a clean one
    @staticmethod
    def compare_clean_installation(cms_type, path):
        # TODO check for the working version of the 'cms_type' installation
        # and download from the Internet a clean one to compare

        return None

    # Scan a website (currently scan only Wordpress sites)
    @staticmethod
    def scan_website(site_type, site_path):
        print("Scanning web site . . . ", end="")
        wordpress = Wordpress(site_path)
        wordpress.scan()
        print("done.")
        print("Reading dictionary . . . ", end="")
        wp_suspect_files = Dictionary.get_suspect_files_by_name(site_type, site_path)
        wp_suspect_content = Dictionary.get_suspect_content_by_content(site_type, site_path)
        print("done.")

        # Searching for suspect files by name
        print("Searching for suspect files (by name) . . . ", end="")
        results = wordpress.find_suspect_files(wp_suspect_files)
        print("done.")

        if len(results) == 0:
            print("No suspect files were found.")
        else:
            print("Suspect files were found. Listing . . .")
            for entry in results:
                print("\t" + entry.path)

            print("done.")

        # Searching for suspect files by content
        print("Searching for suspect files (by content) . . .")
        results = wordpress.find_suspect_content(wp_suspect_content)

        if len(results) == 0:
            print("No suspect content were found")
        else:
            print("Suspect content were found is some file/s. Listing . . .")
            for file in results:
                print("\t" + file + ": " + results[file])

            print("done.")

    @staticmethod
    def add_suspect_file(filename):
        Dictionary.add_suspect_file(filename)
        print("Added '" + filename + "' as a suspect file to the dictionary")

    @staticmethod
    def add_suspect_content(content):
        Dictionary.add_suspect_content(content)
        print("Added '" + content + "' as a suspect word to the dictionary")
