import os
import urllib.request
import fnmatch
from termcolor import colored
from progress.bar import Bar

from CMS import CMS
from Constants import CACHE_DIR

# This class represents a Wordpress installation
class Wordpress(CMS):

    def __init__(self, path, name, log=True):
        super().__init__(path, name, log)

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

        try:
            urllib.request.urlretrieve(url, zip_file, self.download_progress)

            if not os.path.isfile(zip_file):
                return False

            return True
        except Exception as e:
            print(e)
            raise Exception('Some error has produced while downloading a clean installation. Please, check your conectivity.')

    # Progress bar to show clean installation download
    bar = None

    # Update download state using a progressbar
    @staticmethod
    def download_progress(block_count, block_size, total_size):
        global bar

        # First time, progress bar is instantiated
        if Wordpress.bar is None:
            Wordpress.bar = Bar(colored("Downloading a new one (it will be stored for later uses)", "blue"),
                                 fill=colored("#", "blue"), max=total_size, suffix='%(percent)d%%')

        # Calculate how much is downloaded and update progress bar during the whole process
        downloaded = block_count * block_size
        if downloaded < total_size:
            Wordpress.bar.next(block_size)
        else:
            Wordpress.bar.finish()

    # Cleanup the site fixing permissions and removing unnecessary files with information that exposes the website
    # to attackers
    def cleanup_site(self):

        # Fix permissions in folder and files
        os.chmod(self.path, 0o755)
        self.log.info("permissions changed:.:755")
        os.chmod(os.path.join(self.path, ".htaccess"), 0o644)
        self.log.info("permissions changed:.htaccess:644")
        os.chmod(os.path.join(self.path, "wp-config.php"), 0o644)
        self.log.info("permissions changed:wp-config.php:644")
        os.chmod(os.path.join(self.path, "wp-admin"), 0o755)
        self.log.info("permissions changed:wp-admin:755")
        os.chmod(os.path.join(self.path, "wp-content"), 0o755)
        self.log.info("permissions changed:wp-content:755")
        os.chmod(os.path.join(self.path, "wp-includes"), 0o755)
        self.log.info("permissions changed:wp-includes:755")

        # Delete some files that show too more information about current installation
        if os.path.isfile(os.path.join(self.path, "readme.html")):
            os.remove(os.path.join(self.path, "readme.html"))
            self.log.info("file removed:" + os.path.join(self.path, "readme.html"))

        # Search for readme and related files to hide information about current installation and its plugin
        for dirpath, dirnames, filenames in os.walk(self.path):
            # Remove readme files. They show information about plugins/themes version
            for filename in fnmatch.filter(filenames, "*.txt"):
                os.remove(os.path.join(dirpath, filename))
                self.log.info("file removed:" + os.path.join(dirpath, filename))

            # Remove LICENSE files
            for filename in fnmatch.filter(filenames, "LICENSE"):
                os.remove(os.path.join(dirpath, filename))
                self.log.info("file removed:" + os.path.join(dirpath, filename))

            # Remove 'generator' metatag in theme files
            for filename in fnmatch.filter(filenames, "functions.php"):

                if "wp-content/themes" in dirpath:
                    file = open(os.path.join(dirpath, filename), "a")
                    file.write("remove_action('wp_head', 'wp_generator');")
                    file.close()
                    self.log.info("added:'remove_action(\'wp-head\', \'wp_generator\');':enf of file:" +
                                 os.path.join(dirpath, filename))

            # If folder hasn't index.php file, add an extra one with no code to avoid directory listing
            if not os.path.isfile(os.path.join(dirpath, "index.php")):
                file = open(os.path.join(dirpath, "index.php"), "w")
                file.write("<?php\n// masc is protecting your site\n")
                file.close()
                self.log.info("file created:index.php:at:" + dirpath)




