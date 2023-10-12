#!/usr/bin/env python

# Copyright 2023 Hendrik Wingbermuehle, Denys Serdyukov

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# from distutils.core import setup
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