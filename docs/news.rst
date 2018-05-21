News
====

Version 0.1.2 (2018-05-22)
--------------------------

* Fix inpx import: decode filenames to unicode.

Version 0.1.1 (2018-05-17)
--------------------------

* Import all \*.glst files (Flibusta fb2, LibRusEc fb2, non-fb2).

* Convert README.txt to README.rst.

* Import new (17 fields) INP.

Version 0.1.0 (2018-04-25)
--------------------------

* Web-interface: Search for authors, list books by an author,
  download a book.

* Do not allow to run two instances of `ml-web.py` web-interfaces.
  The second instance redirects browser to the first one and exits.

* Option `--download-to` provides the path to the download directory
  in script `ml-search.py`.

Version 0.0.17 (2018-03-24)
---------------------------

* Display progress bar on updating counters.

* Inhibit progress bar if stdout is not terminal.

Version 0.0.16 (2018-03-22)
---------------------------

* Script ``ml-import.py`` displays progress bar.
  Option ``-P`` prevents it.

Version 0.0.15 (2017-04-26)
---------------------------

* Use m_lib.defenc instead of m_lib; install it from PyPI.

* Use pytest, coverage and tox for testing.

Version 0.0.14 (2016-07-29)
---------------------------

* Python 3: support for Py2 and Py3 (3.4+) with one codebase.

Version 0.0.13 (2016-06-11)
---------------------------

* Add option -C|--config file.

* Change options: -D|--database, -P|--path, -F|--format.

Version 0.0.12 (2016-06-09)
---------------------------

* Download many books.

* Pass format of the downloaded file name in the command line.

Version 0.0.11 (2016-06-06)
---------------------------

* Download exactly one book.

Version 0.0.10 (2016-05-31)
---------------------------

* Multidatabase - every script can open a database by pathname or DB URI.

* Print count after the list.

* Rename -d/--details options to -v/--verbose.

Version 0.0.9 (2016-05-30)
---------------------------

* Search authors/extensions/genres/languages by database id.

Version 0.0.8 (2016-05-29)
---------------------------

* Search by author's, book's, extension's, language's id.

* Output count of found objects.

* Use option -d to output database id.

Version 0.0.7 (2016-05-25)
---------------------------

* Extend ml-search.py to search books by authors, extensions, genres,
* languages.

Version 0.0.6 (2016-05-21)
---------------------------

* Extend ml-search.py to search books by title, series, archive, file.

Version 0.0.5 (2016-05-14)
---------------------------

* Extend script ml-search.py to search extensions/genres/languages.

Version 0.0.4 (2016-05-11)
---------------------------

* Command-line script to search authors by surname/name/full name.

Version 0.0.3 (2015-12-24)
---------------------------

* Convert \*.inp(x) to SQL.

Version 0.0.2 (2015-12-21)
---------------------------

* Import genres from glst files.

Version 0.0.1 (2015-12-15)
---------------------------

* The project started. Created DB schema.
