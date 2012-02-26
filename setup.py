#!/usr/bin/env python

# Bootstrap installation of Distribute
from importlib import import_module

import os, sys

from distutils.core import setup


def package_env(file_name, strict=False):
    file_path = os.path.join(os.path.dirname(__file__),file_name)
    if os.path.exists(file_path) or strict:
        return open(file_path).read()
    else:
        return ''

PACKAGE = 'gnss'
PROJECT = 'gnss'
PACKAGE_DIR = 'gnss'

VERSION = package_env('VERSION')
URL = package_env('URL')
AUTHOR_AND_EMAIL = [v.strip('>').strip() for v \
                        in package_env('AUTHOR').split('<mailto:')]
if len(AUTHOR_AND_EMAIL)==2:
    AUTHOR, AUTHOR_EMAIL = AUTHOR_AND_EMAIL
else:
    AUTHOR = AUTHOR_AND_EMAIL
    AUTHOR_EMAIL = ''

DESC = "igs.bkg.bund.de geophysics data parser"


if __name__ == '__main__':
    setup(
        name=PROJECT,
        version=VERSION,
        description=DESC,
        long_description=package_env('README.rst'),
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        url=URL,
        license=package_env('LICENSE'),
        packages=['gnss',],
        package_dir={'gnss':PACKAGE_DIR, 
                     'gnss.products':os.path.join('gnss', 'products'),
                     'gnss.data':os.path.join('gnss', 'data')},
        # include_package_data=True,
        # zip_safe=False,
        # test_suite = 'tests',
        # install_requires=['argparse.extra',],
        classifiers=[
            'License :: OSI Approved',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
        ],
        # entry_points = {
        #  'console_scripts': [
        #      'mypoliscomua = mypoliscomua.deploy:main',
        # ],  },
    )

