# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 03:34:26 2021
@author: Carlos Trujillo
"""

from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.5'
DESCRIPTION = 'This is a module that allows you to connect to the Comscore library developed by Annalect and obtain synthesized information'

with open('english_readme.md', encoding='utf-8') as f:
    long_description_english = f.read()

# Setting up
setup(
    name="pycomscore",
    version=VERSION,
    author="Data house CL",
    author_email="data.analitica@omnicommediagroup.com",
    description=DESCRIPTION,
    long_description=long_description_english,
    long_description_content_type = 'text/markdown',
    packages=find_packages(),
    install_requires=['sqlalchemy', 'pandas', 'pymysql'],
    keywords=['python', 'omnicom', 'sql', 'comscore'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)