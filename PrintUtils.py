from termcolor import colored
from MascEntry import MascEntry

# Some utility methods
def print_green(message, extra=None):
    if extra == "":
        print(colored(message, "green"), end="")
    else:
        print(colored(message, "green"))


def print_red(message, extra=None):
    if extra == "":
        print(colored(message, "red"), end="")
    else:
        print(colored(message, "red"))


def print_blue(message, extra=None):
    if extra == "":
        print(colored(message, "blue"), end="")
    else:
        print(colored(message, "blue"))


def print_debug(message, extra=None):
    if extra == "":
        print(colored("[DEBUG] " + message, "yellow"), end="")
    else:
        print(colored("[DEBUG] " + message, "yellow"))


def print_results(results, data_found_message, data_not_found_message):

    if len(results) == 0:
        print_green(data_not_found_message)
    else:
        print_red(data_found_message)
        for file in results:
            if type(file) is MascEntry:
                print("\t" + file.path)
            else:
                print("\t" + file + ": " + results[file])