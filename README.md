# masc
A malware (web) scanner

[homepage](https://sfaci.github.io/masc)

```bash
usage: masc.py [-h] [--site_type {wordpress,drupal,joomla,magento}]
               [--scan PATH] [--add_file FILENAME] [--add_word STRING]

optional arguments:
  -h, --help            show this help message and exit
  --site_type {wordpress,drupal,joomla,magento}
                        which type of web you want to scan:: wordpress,
                        joomla, drupal or magento
  --scan PATH           Scan an installation at the given PATH
  --add_file FILENAME   Add a suspect file to the dictionary
  --add_word STRING     Add a suspect content to the dictionary
```
