import os

from CMS import CMS


class Wordpress(CMS):
    """This class represents a WordPress installation"""
    def __init__(self, path, name, log=True):

        super().__init__(path, name, log)

        if not os.path.isfile(os.path.join(path, "wp-config.php")):
            raise Exception("Fatal Error. This is not a WordPress installation.")

    def search_suspect_content(self):
        """Search for suspect content in the current installation based on the masc dictionary"""
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

    def get_version(self):
        """Get the version of the current installation"""
        version_line = ""

        with open(os.path.join(self.path, "wp-includes/version.php")) as file:
            for line in file:
                if "$wp_version =" in line:
                    version_line = line.lstrip()
                    break

        slices = version_line.split("'")
        return slices[1]

    def cleanup_site(self):
        """
        Clean up the site fixing permissions and removing unnecessary files with information that exposes
        the website to attackers
        """
        # Generic cleaning for any website
        self.delete_known_files()

        # Fix permissions in folder and files
        os.chmod(self.path, 0o755)
        self.log.info("permissions changed:.:755")
        os.chmod(os.path.join(self.path, ".htaccess"), 0o644)
        self.log.info("permissions changed:" + os.path.join(self.path, "htaccess") + ":644")
        os.chmod(os.path.join(self.path, "wp-config.php"), 0o644)
        self.log.info("permissions changed:" + os.path.join(self.path, "wp-config.php") + ":644")
        os.chmod(os.path.join(self.path, "wp-admin"), 0o755)
        self.log.info("permissions changed:" + os.path.join(self.path, "wp-admin") + ":755")
        os.chmod(os.path.join(self.path, "wp-content"), 0o755)
        self.log.info("permissions changed:" + os.path.join(self.path, "wp-content") + ":755")
        os.chmod(os.path.join(self.path, "wp-includes"), 0o755)
        self.log.info("permissions changed:" + os.path.join(self.path, "wp-includes") + ":755")

        # Delete some known files that show too more information about current installation
        if os.path.isfile(os.path.join(self.path, "readme.html")):
            os.remove(os.path.join(self.path, "readme.html"))
            self.log.info("file removed:" + os.path.join(self.path, "readme.html"))

        # Remove tag info at the index page
        if os.path.isfile(os.path.join(self.path, 'wp-content/themes/functions.php')):
            file = open(os.path.join(self.path, 'wp-content/themes/functions.php'), "a")
            file.write("remove_action('wp_head', 'wp_generator');")
            file.close()
            self.log.info("added:'remove_action(\'wp-head\', \'wp_generator\');':end of file:" +
                          "wp-content/themes/functions.php")
