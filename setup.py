#!/usr/bin/env python

from setuptools import setup, find_packages
from plist17lib import __version__

setup(
    name='plist17lib',
    version=__version__,
    description='Python library to parse Apple\'s bplist17 format into JSON',
    author='hwingb, dserd',
    author_email='',
    url='https://github.com/hwingb/plist17lib',
    py_modules=['plist17lib'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
                'bplist17-parser=cli.run_parser:main',
                'bplist17-writer=cli.create_binary:main',
            ]
    }
)