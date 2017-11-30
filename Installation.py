import sqlite3

# Path where installations databases are stored
INSTALLATIONS_PATH = "installations/"

# This class store information about a CMS installation in a database
# to be able to compare later with itself
class Installation:

    def __init__(self, name, path, cms_type):
        # Name of the installation
        self.name = name
        # Current path where this installation is
        self.path = path
        # Installation type: wodpress, joomla, drupal, magento
        self.cms_type = cms_type

        self.__add_data()


    def __add_data(self):
        connection = sqlite3.connect(INSTALLATIONS_PATH + self.name + ".db")
        sql = "CREATE TABLE entries (id INTEGER PRIMARY KEY AUTOINCREMENT, " + \
            "path TEXT, content TEXT, mtime REAL)"

        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()

        # TODO List installation path and store info in the database

    # TODO return all the installation entries
    def list_entries(self):
        return None

    # TODO check if the given file is part of the original installation
    def is_an_official_entry(self, file):
        return False

    # TODO check for changes in this installation with a previous state
    def check_for_changes(self):
        return False





