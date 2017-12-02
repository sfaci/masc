# A custom website
from CMS import CMS


class Custom(CMS):

    def __init__(self, path, name):
        super().__init__(path, name)

    def search_suspect_content(self):
        pass

    def download_clean_installation(self):
        pass

    def get_version(self):
        pass

    def cleanup_site(self):
        pass