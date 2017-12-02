from CMS import CMS

# This class represents a Joomla installation
class Joomla(CMS):


    def __init__(self, path, name):
        super().__init__(path, name)


    def get_version(self):
        pass


    def download_clean_installation(self):
        pass


    def search_suspect_content(self):
        pass


    def cleanup_site(self):
        pass


