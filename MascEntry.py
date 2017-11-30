# Entry is a filesystem archive, file or directory
class MascEntry:

    # Apparently 'st_creator' and 'st_type' are only available in some Unix (like Unix)
    # so that I have created another '__init__' method
    def __init__(self, name, full_path, size, mode, atime, mtime, ctime, btime, st_type="", creator=""):
        self.name = name
        self.full_path = full_path
        self.size = size
        self.mode = mode
        self.atime = atime
        self.mtime = mtime
        self.ctime = ctime
        self.btime = btime
        self.st_type = st_type
        self.creator = creator

    def __str__(self):
        return self.path

    def get_content(self):
        if self.st_type == "file":
            file = open(self.full_path)
            content = file.read()
            file.close()
            return content
