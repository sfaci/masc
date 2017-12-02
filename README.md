# masc

A malware (web) scanner developed during [CyperCamp](http://www.cybercamp.es) Hackathon 2017

## About

[homepage](https://sfaci.github.io/masc)

[PyPI](https://pypi.python.org/pypi/masc)

## Features

* Scan any website for malware using OWASP WebMalwareScanner checksum and YARA rules databases
* Perform some cleaning operations to improve website protection
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

* Python >= 3
* Some Python libraries
  * python-magic
  * yara-python
```bash
santi@zenbook:$ pip3 install python-magic yara-python
```

## Installation

To install _masc_ on your computer, you can download a [release](https://github.com/sfaci/masc/releases), untar it and try.
You can also install it usign pip ('pip3 install masc')

## Usage

```bash
usage: masc.py [-h] [--site-type {wordpress,drupal,joomla,magento}]
               [--scan PATH] [--name NAME] [--list-backups]
               [--add-file FILENAME] [--add-word STRING] [--clean-up]

optional arguments:
  -h, --help            show this help message and exit
  --site-type {wordpress,drupal,joomla,magento}
                        which type of web you want to scan:: wordpress,
                        joomla, drupal or magento
  --scan PATH           Scan an installation at the given PATH
  --name NAME           Name assigned to the scanned installation
  --list-backups        List local backups
  --rollback            Restore a local backup
  --add-file FILENAME   Add a suspect file to the dictionary
  --add-word STRING     Add a suspect content to the dictionary
  --clean-site          Clean up the site to hide information to attackers
  --clean-cache         Clean masc cache (cache and logs, NO backups)
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
