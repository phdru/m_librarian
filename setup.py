#!/usr/bin/env python

from imp import load_source
from os.path import abspath, dirname, join
from setuptools import setup

versionpath = join(abspath(dirname(__file__)), 'm_librarian', '__version__.py')
m_librarian_version = load_source('m_librarian_version', versionpath)

setup(
    name='m_librarian',
    version=m_librarian_version.__version__,
    description='m_Librarian for LibRusEc/Flibusta libraries',
    long_description=open('README.rst', 'rU').read(),
    long_description_content_type="text/x-rst",
    author='Oleg Broytman',
    author_email='phd@phdru.name',
    url='http://phdru.name/Software/Python/m_librarian/',
    project_urls={
        'Homepage': 'http://phdru.name/Software/Python/m_librarian/',
        'Download': 'https://pypi.org/project/m_librarian/%s/'
        % m_librarian_version.__version__,
        'Documentation':
            'http://phdru.name/Software/Python/m_librarian/docs/',
        'Russian docs':
            'http://phdru.name/Software/Python/m_librarian/docs/ru/',
        'Git repo': 'http://git.phdru.name/m_librarian.git/',
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
    ],
    packages=['m_librarian', 'm_librarian.web'],
    package_data={'m_librarian': [
        'glst/*.txt', 'glst/genres_*.glst',
        'translations/*.mo'
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
        'web': ['bottle', 'Cheetah3'],
    },
)
