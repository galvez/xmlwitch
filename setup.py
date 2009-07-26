#!/usr/bin/env python

from distutils.core import setup

DESCRIPTION="A Python implementation of Ruby's XML Builder using the with statement for simplicity"

setup(name="XMLWitch",
      version="0.1.0",
      description=DESCRIPTION,
      license="GPL",
      author="Jonas Galvez",
      author_email="jonas@codeazur.com.br",
      url="http://github.com/galvez/xmlwitch/",
      py_modules = ['xmlbuilder'],
      platforms="Python 2.5 and later",
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: XML',
        ],)
