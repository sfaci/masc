# A custom website
from CMS import CMS


class Custom(CMS):

    def __init__(self, path, name, type="custom"):
        super().__init__(path, name)
        # Override value in case it's creating a 'anonymous' backup
        self.type = type

    def search_suspect_content(self):
        pass

    def download_clean_installation(self):
        pass

    def get_version(self):
        pass

    def cleanup_site(self):
        pass