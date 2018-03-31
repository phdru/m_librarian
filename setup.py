#!/usr/bin/env python

from imp import load_source
from os.path import abspath, dirname, join
from setuptools import setup

versionpath = join(abspath(dirname(__file__)), 'm_librarian', '__version__.py')
m_librarian_version = load_source('m_librarian_version', versionpath)

setup(name='m_librarian',
      version=m_librarian_version.__version__,
      description='m_Librarian for LibRusEc/Flibusta libraries',
      long_description=open('README.txt', 'rtU').read(),
      long_description_content_type="text/plain",
      author='Oleg Broytman',
      author_email='phd@phdru.name',
      url='http://phdru.name/Software/Python/m_librarian/',
      project_urls={
          'Homepage': 'http://phdru.name/Software/Python/m_librarian/',
          'Download':
              'http://phdru.name/Software/Python/m_librarian/'
              'm_librarian-%s.tar.bz2' % m_librarian_version.__version__,
          'Documentation':
              'http://phdru.name/Software/Python/m_librarian/docs/',
          'Russian docs':
              'http://phdru.name/Software/Python/m_librarian/docs/ru/',
          'Git repo': 'http://git.phdru.name/m_librarian.git/',
      },
      license='GPL',
      keywords=['books', 'library', 'Flibusta', 'LibRusEc', 'lib.rus.ec'],
      platforms="Any",
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
      python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
      install_requires=[
          'SQLObject>=2.2.1; python_version=="2.7"',
          'SQLObject>=3.0.0; python_version>="3.4"',
          'm_lib.defenc>=1.0',
      ],
      extras_require={
          'm_lib': ['m_lib>=3.1'],
          'pbar': ['m_lib>=3.1'],
      },
      )
