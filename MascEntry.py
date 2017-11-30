import magic


# A filesystem entry: file or directory
class MascEntry:

    # Apparently 'st_creator' and 'st_type' are only available in some Unix (like Unix)
    # so, by now, I put 'file' or 'dir' manually checking the type of the entry
    def __init__(self, name, full_path, size, mode, atime, mtime, ctime, st_type, creator=""):
        self.name = name
        self.full_path = full_path
        self.size = size
        self.mode = mode
        self.atime = atime
        self.mtime = mtime
        self.ctime = ctime
        self.st_type = st_type
        self.creator = creator


    # Return the content of a plain text file
    def get_content(self):
        if self.is_plain_text():
            file = open(self.full_path)
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
        mimetype = mg.from_file(self.full_path)
        if mimetype.startswith("text"):
            return True
        else:
            return False


    def __str__(self):
        return self.full_path
