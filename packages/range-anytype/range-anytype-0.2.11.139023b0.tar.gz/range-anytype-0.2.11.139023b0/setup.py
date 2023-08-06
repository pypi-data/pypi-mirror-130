#!/usr/bin/env python
# coding=UTF-8
# Author: cheny0y0<https://github.com/cheny0y0><cyy144881@icloud.com>, REGE<https://github.com/IAmREGE>

import sys
try :
    from setuptools import setup
    import setuptools
except ImportError :
    raise ImportError("setuptools not found! please run 'pip install setuptools'.")

if sys.version[0] == "1" :
    raise SystemError("Python version must be >= 3.0 to install this package")
if sys.version[0] == "2" :
    if sys.version[2] not in ("2", "3", "4", "5", "6", "7") :
        raise SystemError("Python version must be >= 2.2 to install this package")

fh = open("README.md", "r", encoding="utf-8")
long_description = fh.read()
fh.close()

setup(
    name="range-anytype",
    version="0.2.11.139023b",
    description="Range object for any type for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="cheny0y0, REGE",
    author_email="cyy144881@icloud.com",
    url="",
    packages=setuptools.find_packages(),
    
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: Android",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Operating System :: Other OS",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: iOS",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
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
        "Topic :: Software Development :: Libraries"
    ],
    zip_safe=True,
)
