#!/usr/bin/env python
# coding=UTF-8
# Author: cheny0y0<https://github.com/cheny0y0><cyy144881@icloud.com>, REGE<https://github.com/IAmREGE>
from setuptools import setup
import setuptools

fh = open("README.md", "r", encoding="utf-8")
long_description = fh.read()
fh.close()

setup(
    name="key-pressing",
    version="0.1.3.132321b",
    description="Key pressing detecting for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="cheny0y0, REGE",
    author_email="cyy144881@icloud.com",
    url="",
    packages=setuptools.find_packages(),
    
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: iOS",
        "Programming Language :: Python",
#        "Programming Language :: Python :: 1",
#        "Programming Language :: Python :: 1.6",
        "Programming Language :: Python :: 2",
#        "Programming Language :: Python :: 2.0",
#        "Programming Language :: Python :: 2.1",
#        "Programming Language :: Python :: 2.2",
        "Programming Language :: Python :: 2.3",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    zip_safe=True,
)
