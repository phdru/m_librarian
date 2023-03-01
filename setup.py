#!/usr/bin/env python

from os.path import abspath, dirname, join
from setuptools import setup
import sys

versionpath = join(abspath(dirname(__file__)), 'm_librarian', '__version__.py')
m_librarian_version = {}

if sys.version_info[:2] == (2, 7):
    execfile(versionpath, m_librarian_version)  # noqa: F821 'execfile' Py3

elif sys.version_info >= (3, 4):
    exec(open(versionpath, 'r').read(), m_librarian_version)

else:
    raise ImportError("m_librarian requires Python 2.7 or 3.4+")

setup(
    name='m_librarian',
    version=m_librarian_version['__version__'],
    description='m_Librarian for LibRusEc/Flibusta libraries',
    long_description=open('README.rst', 'r').read(),
    long_description_content_type="text/x-rst",
    author='Oleg Broytman',
    author_email='phd@phdru.name',
    url='https://phdru.name/Software/Python/m_librarian/',
    project_urls={
        'Homepage': 'https://phdru.name/Software/Python/m_librarian/',
        'Download': 'https://pypi.org/project/m_librarian/%s/'
        % m_librarian_version['__version__'],
        'Documentation':
            'https://phdru.name/Software/Python/m_librarian/docs/',
        'Russian docs':
            'https://phdru.name/Software/Python/m_librarian/docs/ru/',
        'Git repo': 'https://git.phdru.name/m_librarian.git/',
        'Github repo': 'https://github.com/phdru/m_librarian',
        'Issue tracker': 'https://github.com/phdru/m_librarian/issues',
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
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    packages=['m_librarian', 'm_librarian.web'],
    package_data={'m_librarian': [
        'glst/*.txt', 'glst/genres_*.glst',
        'translations_dir/*.mo', 'translations_dir/*.po',
        'web/static/style.css', 'web/views/*.py', 'web/views/*.tmpl',
        ]
    },
    scripts=['scripts/ml-import.py', 'scripts/ml-initdb.py',
             'scripts/ml-search.py', 'scripts/ml-web.py'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=[
        'SQLObject>=2.2.1; python_version=="2.7"',
        'SQLObject>=3.0.0; python_version>="3.4"',
        'm_lib.defenc>=1.0',
    ],
    extras_require={
        'pbar': ['m_lib>=3.1'],
        'web': ['bottle', 'CT3'],
    },
)
