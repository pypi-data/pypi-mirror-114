#!/usr/bin/env python
import os
from setuptools import setup, find_packages
from version import __version__

##from setuptools_scm import get_version

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

exec(open('version.py').read())


setup(
    name="nuphy2",
    description="Automatically created environment for python package",
    url="http://gitlab.com/jaromrax/nuphy2",
    author="JM",
    author_email="jaromrax@gmail.com",
    licence="",
    version=__version__,
    packages=find_packages(),
    package_data={'nuphy2': ['data/*']},
    packagedata={'nuphy2': ['data/*']},
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    scripts = ['bin/nuphy2'],
    install_requires = ['numpy==1.16.2'],
)
#
#   To Access Data in Python: :
#   DATA_PATH = pkg_resources.resource_filename('nuphy2', 'data/')
#   DB_FILE =   pkg_resources.resource_filename('nuphy2', 'data/file')
