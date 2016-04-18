#!/usr/bin/env python
from setuptools import setup

long_description = open('README.rst').read()

setup(name="nimsp",
      version='0.4.1',
      py_modules=["nimsp"],
      description="Library for interacting with the National Institute on Money in State Politics API",
      author="Michael Stephens",
      author_email="mstephens@sunlightfoundation.com",
      license="BSD",
      url="http://github.com/sunlightlabs/python-nimsp",
      long_description=long_description,
      platforms=["any"],
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   ],
      )
