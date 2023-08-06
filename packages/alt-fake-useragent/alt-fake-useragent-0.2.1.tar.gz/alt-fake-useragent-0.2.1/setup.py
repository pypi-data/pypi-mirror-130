# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import io
import os
import re

from setuptools import setup, find_packages


def get_version():
    regex = r"__version__\s=\s\'(?P<version>[\d\.]+?)\'"

    path = ('fake_useragent', 'settings.py')

    try:
        return re.search(regex, read(*path)).group('version')
    except:
        
        from fake_useragent.settings import __version__
        
        return __version__


def read(*parts):
    return open('README.md').read()

setup(
    name='alt-fake-useragent',
    version=get_version(),
    author='botmakerdeveloper@gmail.com',
    author_email='botmakerdeveloper@gmail.com',
    url='https://github.com/MrBotDeveloper/Fake-UserAgent-Alternate',
    description='A Fixed and Updated Alternative for fake-useragent',
    long_description_content_type="text/markdown",
    long_description=read('README.md'),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    keywords=[
        'user', 'agent', 'user agent', 'useragent',
        'fake', 'alternate fake useragent', 'fake user agent',
        'fixed fake useragent', 'python requests',
    ],
)
