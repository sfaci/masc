# masc

A malware (web) scanner developed during [CyperCamp](http://www.cybercamp.es) Hackathon 2017

## About

[homepage](https://sfaci.github.io/masc)

[PyPI](https://pypi.python.org/pypi/masc)

## Features

* Scan any website for malware using OWASP WebMalwareScanner checksum and YARA rules databases
* Perform some cleaning operations to improve website protection
* Monitor the website for changes. Details are written in a log file
* Custom website support
  * Scan your site to know if it has been infected with some malware
  * List your local backups
  * Logging support
  * Backup your site
  * Restore website
* WordPress support
  * Scan your site to know if it has been infected with some malware
  * Scan for suspect files and compare with a clean installation
  * Clean up your site to avoid giving extra information to attackers
  * Backup your site (to recover later if you need)
  * List your local backups
  * Logging support
  * Restore website

## Requirements

First of all, notice that this tool is developed under Linux and, at the moment, it has been tested only under this Operating System

* Python >= 3
* Some Python libraries
  * python-magic
  * yara-python
  * watchdog
  * termcolor
```bash
santi@zenbook:$ pip3 install python-magic yara-python watchdog termcolor
```

#### Notice

_masc_ is developed under Linux and it has not been tested under any other Operating System.

Anyway, it should run without problems under any Unix-friendly OS. In particular, in Mac OSX I have noticed it's neccesary to install
[Homebrew](https://brew.sh) to use python-magic library propery as _libmagic_. Check first the previous link to the _brew_ homepage and then
you will be able to install as I show below:

```bash
santi@zenbook:$ brew install libmagic
```

## Installation

To install _masc_ on your computer, you can download a [release](https://github.com/sfaci/masc/releases), untar it and try.
You can also install it usign pip ('pip3 install masc')

## Usage

```bash

masc 0.1 (http://github.com/sfaci/masc)
usage: masc.py [-h] [--add-file FILENAME] [--add-word STRING] [--clean-cache]
               [--clean-site] [--list-backups] [--list-logs] [--make-backup]
               [--monitor] [--name NAME] [--rollback] [--scan PATH]
               [--site-type {wordpress,drupal,custom}]

optional arguments:
  -h, --help            show this help message and exit
  --add-file FILENAME   Add a suspect file to the dictionary
  --add-word STRING     Add a suspect content to the dictionary
  --clean-cache         Clean masc cache (cache and logs files, NO backups)
  --clean-site          Clean up the site to hide information to attackers
  --list-backups        List local backups
  --make-backup         Create a local backup of the current installation
  --monitor             Monitor site to detect changes
  --name NAME           Name assigned to the scanned installation
  --rollback            Restore a local backup
  --scan PATH           Scan an installation at the given PATH
  --site-type {wordpress,drupal,custom}
                        which type of web you want to scan:: wordpress,
                        joomla, drupal or magento
```

## Test

There is a repository in the Docker Hub to perform tests [masc-wordpress](https://hub.docker.com/r/sfaci/masc-wordpress/)

## Documentation

You can find a complete tutorial about how to use _masc_ in the [wiki](https://github.com/sfaci/masc/wiki)

## Thanks

Thanks to [OWASP WebMalwareScanner](https://github.com/maxlabelle/WebMalwareScanner) for some ideas and the signatures databases with checksums and YARA
rules (and how to load it to work with). 

## Author

Santiago Faci <santiago.faci@gmail.com>
