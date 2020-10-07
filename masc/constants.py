import os

"""
Some contants to use
"""

# Current path that masc is being executed from
BASE_PATH = os.path.dirname(os.path.realpath(__file__))

# This is the local directory where I make some test with fake websites
TEST_DIR = "test/"

# Differents local path to make some tests
WORDPRESS_DIR = TEST_DIR + "wordpress/"
JOOMLA_DIR = TEST_DIR + "joomla/"
DRUPAL_DIR = TEST_DIR + "druptal/"
MAGENTO_DIR = TEST_DIR + "magento/"

# The dir where clean installations are downloaded and unzipped
CACHE_DIR = os.path.expanduser("~/.masc/cache/")

# The dir where backups are stored
BACKUPS_DIR = os.path.expanduser("~/.masc/backups/")

# Logs dir
LOGS_DIR = os.path.expanduser("~/.masc/logs/")
