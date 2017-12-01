import magic
import re


# A filesystem entry: file or directory with some information
class MascEntry:

    # Apparently 'st_creator' and 'st_type' are only available in some Unix (like Unix)
    # so, by now, I put 'file' or 'dir' manually checking the type of the entry
    def __init__(self, name, path, absolute_path, size, mode, atime, mtime, ctime, st_type, creator=""):
        # The name of the file (without path)
        self.name = name
        # The relative path to file
        self.path = path
        # The absolute path to file
        self.absolute_path = absolute_path
        # The file zie
        self.size = size
        self.mode = mode
        self.atime = atime
        self.mtime = mtime
        self.ctime = ctime
        self.st_type = st_type
        self.creator = creator


    # Return the content if it's a plain text file
    def get_content(self):
        if not self.is_plain_text():
            return None

        file = open(self.absolute_path)
        content = file.read()
        file.close()
        return content


    # Check if the entry is a file
    def is_file(self):
        if self.st_type == "file":
            return True
        else:
            return False


    # Check if the entry is a plain text file
    def is_plain_text(self):
        if not self.is_file():
            return False

        mg = magic.Magic(mime=True)
        mimetype = mg.from_file(self.absolute_path)
        if mimetype.startswith("text"):
            return True
        else:
            return False


    # Check if the filename (without extension) ends with a number
    def name_ends_with_digits(self):

        if re.search(r'\d+$', self.name.split(".")[0]) is None:
            return False

        return True

    # string representation of an entry
    def __str__(self):
        return self.absolute_path
