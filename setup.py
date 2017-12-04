from distutils.core import setup
from pypandoc.pandoc_download import download_pandoc
import pypandoc

# generate README.txt from README.md
# download_pandoc()     # it only works under Mac OS X. With Debian, it crashes
readme = pypandoc.convert_file('README.md', 'rst')
file_readme = open('README.txt', 'w+')
file_readme.write(readme)
file_readme.close()

setup(
    name='masc',
    version='0.2.1',
    packages=['', ],
    license='GNU GENERAL PUBLIC LICENSE Version 3',
    description='A malware web scanner',
    long_description=open('README.txt').read(),
    author='Santiago Faci',
    author_email='santiago.faci@gmail.com',
    url='http://github.com/sfaci/masc',
    download_url='https://github.com/sfaci/masc/releases/download/masc-0.2.2/masc-0.2.2.tar.gz',
    keywords='malware scanner security',
    classifiers=['Development Status :: 3 - Alpha'],
    requires=['watchdog', 'yara', 'magic', 'termcolor', 'pypandoc']
)
