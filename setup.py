#!/usr/bin/env python

from imp import load_source
from os.path import abspath, dirname, join

try:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup
    is_setuptools = True
except ImportError:
    from distutils.core import setup
    is_setuptools = False

versionpath = join(abspath(dirname(__file__)), 'm_librarian', '__version__.py')
load_source('m_librarian_version', versionpath)
from m_librarian_version import __version__

setup(name='m_librarian',
      version=__version__,
      description='Librarian for LibRusEc/Flibusta libraries',
      long_description=open('README.txt', 'rtU').read(),
      author='Oleg Broytman',
      author_email='phd@phdru.name',
      url='http://phdru.name/Software/Python/',
      license='GPL',
      packages=['m_librarian'],
      requires=['SQLObject'],
      )
