# masc

<img align="left" height="200px" width="200px" src="https://www.arkabytes.com/img/masc.jpg">

A malware (web) scanner developed during [CyperCamp](http://www.cybercamp.es) Hackathon 2017

## About

[homepage](https://sfaci.github.io/masc)

[PyPI](https://pypi.python.org/pypi/masc)

## Features

At the moment, there are some features avaiable for any type of website (custom or CMS) and some of them only available for specific
platforms:

* Scan any website for malware using OWASP WebMalwareScanner checksum, YARA rules databases and ClamAV engine (if available)
* Perform some cleaning operations to improve website protection
* Monitor the website for changes. Details are written in a log file
* Scan your site to know if it has been infected with some malware
* List your local backups
* Logging support
* Backup your site
* Restore website
* Scan for suspect files and compare with a clean installation (for Wordpress and Drupal)
* Clean up your site to avoid giving extra information to attackers (only available for Wordpress)

## Installation

To install _masc_ on your computer, you can simply clone this repository.
You can also download the latest [release](https://github.com/sfaci/masc/releases), untar it and try. Or maybe you prefer to install it usign pip ('pip3 install masc').

Check [requirements](https://github.com/sfaci/masc#requirements) before run it.
Check [this notice](https://github.com/sfaci/masc#notice) before if you are using Debian Linux.
Check [this notice](https://github.com/sfaci/masc#notice-1) before if you are using Mac OSX.

masc has been tested only in Linux and Mac OSX platforms. It should run under Windows but I don't have tried yet.

### Requirements

First of all, notice that this tool is developed under Linux and Mac OSX environments and, at the moment, it has been tested only under these Operating Systems

* Python >= 3
* Some Python libraries
  * python-magic
  * yara-python
  * watchdog
  * termcolor
  * pypandoc
  * progress
  * pyclamd
  
```bash
santi@zenbook:$ pip3 install python-magic yara-python watchdog termcolor pypandoc progress pyclamd
```
* ClamAV to integrate with its engine (optional but recommended)

#### Notice for Debian users/developers

In my notebook, after upgrading to Debian testing, masc became to show an error related to Yara

```bash
OSError: /usr/lib/libyara.so: cannot open shared object file: No such file or directory
```

After trying a lot of solutions I found in the Internet, I realized that this file was located in my computer in 
_/usr/local/lib/python3.5/dist-packages/usr/lib_, so I created a symbolic link from the previous path to _/usr/lib_

```bash
santi@zenbook:$ ln -s /usr/local/lib/python3.5/dist-packages/usr/lib/libyara.so /usr/lib/libyara.so
```

And now, masc and Yara library are running with no problems.

#### Notice for MacOS users/developers

_masc_ is developed under Linux but it has been tested under Mac OSX. Anyway, it should run without problems under any Unix-friendly OS. 

In particular, in Mac OSX I have noticed it's neccesary to install
[Homebrew](https://brew.sh) to use python-magic library properly as _libmagic_. Check first the previous link to the _brew_ homepage and then
you will be able to install as I show below:

```bash
santi@zenbook:$ brew install libmagic
```

Also, in my computer I had to change the first line of the _masc.py_ script. Python3 is installed in _/usr/local/bin_ and it's not 
allowed to create symlinks from _/usr/bin_ 

Change the first line in _masc.py_

```bash
#!/usr/bin/python3
```

for this line

```bash
#!/usr/local/bin/python3
```

Anyway, you always can run _masc_ using the Python interpreter instead running the script directly:

```bash
santi@zenbook:$ python3 masc.py
```

## Usage

```bash

masc 0.2.2 (http://github.com/sfaci/masc)
usage: masc.py [-h] [-af FILENAME] [--aw STRING] [-cc] [-c] [-l] [-b] [-m]
               [-n NAME] [-p PATH] [-r] [-s] [-t {wordpress,drupal,custom}]

optional arguments:
  -h, --help            show this help message and exit
  -af FILENAME, --add-file FILENAME   
                        Add a suspect file to the dictionary
  -aw STRING --add-word STRING     
                        Add a suspect content to the dictionary
  -cc, --clean-cache        Clean masc cache (cache and logs files, NO backups)
  -c, --clean-site          Clean up the site (and apply some extra actions to hide information to attackers)
  -l, --list-backups        List local backups
  -b, --make-backup         Create a local backup of the current installation
  -m, --monitor             Monitor site to detect changes
  -n NAME, --name NAME      Name assigned to the scanned installation
  -p PATH, --path PATH      Website installation path
  -r, --rollback            Restore a local backup
  -s, --scan                Scan website for malware
  -t {wordpress,drupal,custom}, --site-type {wordpress,drupal,custom}
                        which type of web you want to scan:: wordpress,
                        joomla, drupal or magento
```

The actions you can perform over a web installation are:

* -s, --scan (with or without the option --clean-site)
* -r, --rollback (with its options)
* -m, --monitor (with its options)
* -b, --make-backup (with its options)
* -l, --list-backups

And you have to consider that if you want to perform some actions over some kind of web installation, it's mandatory to
specify the type (-t or --type) and path (-p or --path).

For instance, if you have a WordPress installation in /var/www/html and you want to scan it entirely:

```
santi@zenbook:$ ./masc.py --scan --site-type wordpress --path /var/www/html
```

And if you want to perform clean up actions (to remove some malware, for instance):

```
santi@zenbook:$ ./masc.py --scan --site-type wordpress --path /var/www/html --clean-site
```

## Test

There is a repository in the Docker Hub to perform tests [masc-wordpress](https://hub.docker.com/r/sfaci/masc-wordpress/)

In addition, there are two samples of hacked websites in the samples zip file:

 * **drupal**: clean Drupal installation with some malware scripts. You can use it to make 
 your test during development
 * **wordpress**: clean WodPress installation with some malware to test. There is also some security holes such as
 emtpy directories and some permissions wrong to test the extra features implemented to this kind of CMS

## Documentation

You can find a tutorial about how to use _masc_ at the [wiki](https://github.com/sfaci/masc/wiki)

## How to contribute

If you want to contribute to this project, take a look at the [wiki](https://github.com/sfaci/masc/wiki). 
There is a section about [How to contribute to this project](https://github.com/sfaci/masc/wiki/How-to-contribute)

## Thanks

Thanks to [OWASP WebMalwareScanner](https://wiki.owasp.org/index.php/OWASP_Web_Malware_Scanner_Project) for some ideas 
and the signatures databases with checksums and YARA
rules (and how to load it to work with). 

## Author

Santiago Faci <santi@arkabytes.com>
