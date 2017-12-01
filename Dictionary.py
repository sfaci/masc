DICTS_PATH = "dicts/"
WP_SUSPECT_FILES_DATA = DICTS_PATH + "wp_suspect_files.data"
WP_SUSPECT_CONTENT_DATA = DICTS_PATH + "wp_suspect_content.data"

class Dictionary:

    suspect_files = []
    suspect_content = []

    # Return suspect files for an specific type of installation: wordpress, joomla, . . .
    @classmethod
    def load_suspect_files(cls, type, path):
        if type == "wordpress":
            with open(WP_SUSPECT_FILES_DATA) as file:
                for line in file:
                    if line.startswith("#"):
                        continue
                    cls.suspect_files.append(path + line.rstrip())
        # TODO More CMS


    @classmethod
    def load_suspect_content(cls, type, path):
        if type == "wordpress":
            with open(WP_SUSPECT_CONTENT_DATA) as file:
                for line in file:
                    if line.startswith("#"):
                        continue;
                    cls.suspect_content.append(line.rstrip())
        # TODO More CMS


    @classmethod
    def load_signatures(cls):
        pass


    @staticmethod
    def add_suspect_file(filename):
        with open(WP_SUSPECT_FILES_DATA, "a") as file:
            file.write(filename + "\n")

    @staticmethod
    def add_suspect_content(content):
        with open(WP_SUSPECT_CONTENT_DATA, "a+") as file:
            file.write(content + "\n")
