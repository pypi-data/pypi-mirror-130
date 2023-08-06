#!/usr/bin/env python3

import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

NAME = 'refery'
SCRIPTS = ['bin/refery']
VERSION = '1.0.0'
DESCRIPTION = 'Functional testing tool'
AUTHOR = 'Rostan Tabet'
EMAIL = 'rostan.tabet@gmail.com'
REQUIRED = ['PyYAML', 'colorama']

setup(
    name=NAME,
    scripts=SCRIPTS,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    packages=['src'],
    install_requires=REQUIRED,
    long_description=README,
    long_description_content_type='text/markdown',
)
