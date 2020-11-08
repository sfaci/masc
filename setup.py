from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='masc',
    version='0.2.2',
    author='Santiago Faci',
    author_email='santiago.faci@gmail.com',
    description='A malware web scanner',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sfaci/masc',
    packages=['masc'],
    keywords='malware scanner security',
    package_data={
        'masc': [
            'dicts/*',
            'signatures/checksum/*',
            'signatures/rules/*',
            'masc.conf',
        ]
    },
    entry_points={
        'console_scripts': [
            'masc=masc.main:main',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    install_requires=[
        'watchdog',
        'yara-python',
        'python-magic',
        'termcolor',
        'pyclamd',
        'progress',
        'importlib-metadata;python_version<"3.8"',
    ],
)
