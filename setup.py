#!/usr/bin/env python

from distutils.core import setup

DESCRIPTION = "A Python implementation of Ruby's XML Builder using the with statement for simplicity"

setup(name="xmlwitch",
      version="0.1.0",
      description=DESCRIPTION,
      license="BSD",
      author="Jonas Galvez",
      author_email="jonas@codeazur.com.br",
      url="http://github.com/galvez/xmlwitch/tree/master",
      py_modules = ['xmlwitch'],
      platforms="Python 2.5 and later",
      classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: XML'
        ],)