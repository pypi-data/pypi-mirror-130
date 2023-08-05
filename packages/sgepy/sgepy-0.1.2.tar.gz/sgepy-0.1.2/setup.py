#!/usr/bin/env python
from setuptools import setup, find_packages
import os
import glob
import codecs

# dependencies
install_reqs = [
    'dill>=0.3',
    'pathos>=0.2.8',
    'tqdm>=4'
]

# getting version from __init__.py
def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError('Unable to find version string.')
    
## install main application
desc = 'sgepy package'
setup(
    name = 'sgepy',
    version = get_version('sgepy/__init__.py'),
    description = desc,
    long_description = desc + '\n See README for more information.',
    author = 'Nick Youngblut',
    author_email = 'nyoungb2@gmail.com',
    install_requires = install_reqs,
    license = 'MIT license',
    packages = find_packages(),
    package_dir={'sgepy': 'sgepy'},
    scripts = ['bin/sgepy-test.py'],
    url = 'https://github.com/nick-youngblut/sgepy'
)




