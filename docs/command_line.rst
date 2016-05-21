
Command-line scripts
====================


.. contents::
   :local:


ml-initdb.py
------------

Initialize database and import genres list. Doesn't really needed as
the next script does all that too.


ml-import.py
------------

Usage::

    ml-import.py [file.inpx ...]

Initialize database, import genres list and import a list of INPX files
listed in the command line. On subsequent runs doesn't destroy DB or
reimport genres; it also skips already import books but import new ones.


ml-search.py
------------

Usage::

    ml-search.py [-i] [-I] [-t] [-s] [-f] ...

Search through the database and display results. Currently can only
search authors by name.

Global options::

    -i, --ignore-case     ignore case (default is to guess)
    -I, --case-sensitive  don't ignore case
    -t, --start           search type: substring at the start
                          (this is the default)
    -s, --substring       search type: substring anywhere
    -f, --full            search type: match the full string

Options ``-i/-I`` cannot be used together as they are the opposite. In
case none of them are used the program guesses case-sensitivity by
looking at the arguments. If all arguments are lowercase the program
performs case-insensitive search. If there are UPPERCASE or MixedCase
arguments the program performs case-sensitive search.

Options ``-t/-s/-f`` define the search type. Search types are:

* start - search for substring at the start of the search field; for
  example searching for "duck" returns results for "duck" and "duckling"
  but not for "McDuck"; this is the default search type.
* substring - search for any substring; "duck" => "duck", "duckling",
  "McDuck" (except for case-sensitive search, of course).
* full - search for exact match, compare the entire strings;
  i.e. searching for "duck" returns results for "duck" but not for
  "duckling";


Author search
^^^^^^^^^^^^^

Usage::

    ml-search.py [-i/-I] [-t/-s/-f] author [-s surname] [-n name] [-m misc-name] [fullname]

Search and print a list of authors by surname/name/misc name/full name.

Options::

    -s, --surname surname       Search by surname
    -n, --name name             Search by name
    -m, --misc-name misc. name  Search by misc. name

Example::

    ml-search.py -i author -s duck

Search and print a list of authors whose surname starts with "duck",
case insensitive.

If a few options are given the search is limited with operator AND.
Example::

    ml-search.py -i author -s duck -n mack

Search and print a list of authors whose surname starts with "duck", and
name starts with "mack", case insensitive.


Book search
^^^^^^^^^^^

Usage::

    ml-search.py [-i/-I] [-t/-s/-f] books [-t title] [-s series] [-a archive] [-f file] [-d]

Search and print a list of books by title, series, archive or file name.

Options::

    -t, --title title      Search by title
    -s, --series series    Search by series
    -a, --archive archive  Search by archive (zip file)
    -f, --file file        Search by file name (without extension)
    -d, --details          Output more details about books;
                           repeat for even more details

By default the program prints only titles of the found book. With one
option `-d` it also prints the list of authors and genres, and also
series the book belongs to (if any) and the serial number of the book in
the series. With two options `-d` (`-d -d` or simply `-dd`) it also
prints the file date and language. With three `-d` it prints archive
name, file name, extension and size, and flag if the book is marked to
be deleted.


Extension search
^^^^^^^^^^^^^^^^

Usage::

    ml-search.py [-i/-I] [-t/-s/-f] ext [name]

Search and print a list of extensions by name.


Genres search
^^^^^^^^^^^^^

Usage::

    ml-search.py [-i/-I] [-t/-s/-f] genres [-n name] [-t title]

Search and print a list of genres by name and title.

Options::

    -n, --name name    Search by name
    -t, --title title  Search by title


Language search
^^^^^^^^^^^^^^^

Usage::

    ml-search.py [-i/-I] [-t/-s/-f] lang [name]

Search and print a list of languages by name.

.. vim: set tw=72 :
