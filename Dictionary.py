DICTS_PATH = "dicts/"
WP_SUSPECT_FILES_DATA = DICTS_PATH + "wp_suspect_files.data"
WP_SUSPECT_CONTENT_DATA = DICTS_PATH + "wp_suspect_content.data"

class Dictionary:

    # Return suspect files for an specific type of installation: wordpress, joomla, . . .
    @staticmethod
    def get_suspect_files_by_name(type, path):

        files = []

        if type == "wordpress":
            with open(WP_SUSPECT_FILES_DATA) as file:
                for line in file:
                    if line.startswith("#"):
                        continue
                    files.append(path + line.rstrip())

        return files

    @staticmethod
    def get_suspect_content_by_content(type, path):

        files = []

        if type == "wordpress":
            with open(WP_SUSPECT_CONTENT_DATA) as file:
                for line in file:
                    if line.startswith("#"):
                        continue;
                    files.append(line.rstrip())

        return files

    @staticmethod
    def add_suspect_file(filename):
        with open(WP_SUSPECT_FILES_DATA, "a") as file:
            file.write(filename + "\n")

    @staticmethod
    def add_suspect_content(content):
        with open(WP_SUSPECT_CONTENT_DATA, "a+") as file:
            file.write(content + "\n")
