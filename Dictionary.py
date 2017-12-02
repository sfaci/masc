import os
import json
import yara
from PrintUtils import print_red, print_blue

DICTS_PATH = "dicts/"
SIGNATURES_PATH = "signatures/"

SUSPECT_FILES_DATA = "_suspect_files.data"
SUSPECT_CONTENT_DATA = "_suspect_content.data"
CHECKSUM_PATH = SIGNATURES_PATH + "checksum/"
RULES_PATH = SIGNATURES_PATH + "rules/"

class Dictionary:

    suspect_files = []
    suspect_content = []
    signatures_db = {}
    yara_rules = []

    # Return suspect files for an specific type of installation: wordpress, joomla, . . .
    @classmethod
    def load_suspect_files(cls, type, path):

        with open(os.path.join(DICTS_PATH, type + SUSPECT_FILES_DATA)) as file:
            for line in file:
                if line.startswith("#"):
                    continue
                cls.suspect_files.append(path + line.rstrip())


    @classmethod
    def load_suspect_content(cls, type, path):
            with open(os.path.join(DICTS_PATH, type + SUSPECT_CONTENT_DATA)) as file:
                for line in file:
                    if line.startswith("#"):
                        continue;
                    cls.suspect_content.append(line.rstrip())


    # Load signatures (checksums and YARA rules) to create the signatures dictionary
    @classmethod
    def load_signatures(cls):

        errors = False

        for entry in os.scandir(CHECKSUM_PATH):
            file_data = open(entry.path).read()
            signatures = json.loads(file_data)

            for signature_hash in signatures["Database_Hash"]:
                cls.signatures_db[signature_hash["Malware_Hash"]] = signature_hash["Malware_Name"]

        print_blue("Loaded " + str(len(cls.signatures_db)) + " malware signatures")

        for entry in os.scandir(RULES_PATH):
            try:
                rules = yara.compile(filepath=entry.path)
                cls.yara_rules.append(rules)
            except:
                errors = True

        if errors:
            print_red("Some errors while reading yara rules. Some rules were not loaded")

        print_blue("Loaded " + str(len(cls.yara_rules)) + " YARA rules")


    @staticmethod
    def add_suspect_file(filename):
        with open(WP_SUSPECT_FILES_DATA, "a") as file:
            file.write(filename + "\n")


    @staticmethod
    def add_suspect_content(content):
        with open(WP_SUSPECT_CONTENT_DATA, "a+") as file:
            file.write(content + "\n")
