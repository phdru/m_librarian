#!/usr/bin/env python

from imp import load_source
from os.path import abspath, dirname, join

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

versionpath = join(abspath(dirname(__file__)), 'm_librarian', '__version__.py')
load_source('m_librarian_version', versionpath)
# Ignore: E402 module level import not at top of file
from m_librarian_version import __version__  # noqa

setup(name='m_librarian',
      version=__version__,
      description='m_Librarian for LibRusEc/Flibusta libraries',
      long_description=open('README.txt', 'rtU').read(),
      author='Oleg Broytman',
      author_email='phd@phdru.name',
      url='http://phdru.name/Software/Python/m_librarian/',
      license='GPL',
      platforms=['POSIX'],
      keywords=['books', 'library', 'Flibusta', 'LibRusEc', 'lib.rus.ec'],
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Natural Language :: English',
          'Natural Language :: Russian',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      packages=['m_librarian'],
      package_data={'m_librarian': [
          'glst/*.txt', 'glst/genres_*.glst',
          'translations/*.mo'
          ]
      },
      scripts=['scripts/ml-import.py', 'scripts/ml-initdb.py',
               'scripts/ml-search.py'],
      )
