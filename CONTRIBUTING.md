# How to contribute to masc

## Getting started

If you want to contribute to this project, first take a look to the opened [issues](https://github.com/sfaci/masc/issues).
There are some bugs already knowns and also some interesting features to include to this project.

In addition, of course, you can make your own proposal as a new issue to work on it. 

## Requirements for coding

You have to take a look to the [Requirements](https://github.com/sfaci/masc#requirements) to find all you need to 
run this project. If you want to contribute on it, you only need a Python IDE (I use [PyCharm CE](https://www.jetbrains.com/pycharm/)).

## Samples (hacked websites)

There are two samples of hacked websites in the **samples** zip file:

 * **drupal**: clean Drupal installation with some malware scripts. You can use it to make 
 your test during development
 * **wordpress**: clean WodPress installation with some malware to test. There is also some security holes such as
 emtpy directories and some permissions wrong to test the extra features implemented to this kind of CMS

## Code structure

* **dicts**: Folder where custom dictionaries are saved
* **docs**: Some documentation about the project
* **icons**: Project icons for GitHub
* **samples**: Samples of hacked websites to test masc
* **signatures**: checksums and Yara rules to use with masc. If you have a new one, you can copy it here. Masc loads the entire folder every time it scans a website
* **CMS.py**: Abstract class to define and implement common behaviour for every website
* **Constants.py**: Some constants
* **Custom.py**: Specific class to implement custom website behaviour
* **Dictionary.py**: Some methods to manage custom dictionaries
* **Drupal.py**: Specific class to implement Drupal website behaviour
* **Joomla.py**: Specific class to implement Joomla website behaviour (currently it's ready but empty)
* **masc.conf**: Configuration file
* **masc.py**: the main executable script
* **MascEntry.py**: A class where a filesystem entry is defined
* **MascUtils.py**: Some static methods to perform some tasks
* **PrintUtils.py**: Some methods to print messages with different colors and manners
* **setup.py**: Setup file to package masc (pypi)
* **virustotal_test.py**: A script to test how integrate masc with virustotal. It works but this feature is not included yet
* **Wordpress.py**: Specific class to implement WordPress website behaviour

In addition, in some cases when you run masc, some folders and files may be created:

* **backups**: Directory where backups are stored
* **cache**: Directory when CMS clean installations are stored 
* **logs**: Directory when application logs are stored