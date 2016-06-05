
Command-line scripts
====================


.. contents::
   :local:


ml-initdb.py
------------

Usage::

    ml-initdb.py [-d]

Options::

    -d, --database database  Open this database by pathname/db uri

Initialize database and import genres list. Isn’t really needed as
the next script does all that too.


ml-import.py
------------

Usage::

    ml-import.py [-d] [file.inpx ...]

Options::

    -d, --database database  Open this database by pathname/db uri

Initialize database, import genres list and import a list of INPX files
listed in the command line. On subsequent runs doesn’t destroy DB or
reimport genres; it also skips already import books but import new ones.


ml-search.py
------------

Usage::

    ml-search.py [-d] [-i] [-I] [-t] [-s] [-f] [-v] [-c] ...

Search through the database and display results. Currently can only
search authors by name.

Global options::

    -d, --database database  Open this database by pathname/db uri
    -i, --ignore-case        ignore case (default is to guess)
    -I, --case-sensitive     don’t ignore case
    -t, --start              search type: substring at the start
                             (this is the default)
    -s, --substring          search type: substring anywhere
    -f, --full               search type: match the full string
    -c, --count              Output count of found objects
    -v, --verbose            Output more details about found objects;
                             repeat for even more details

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

    ml-search.py author [-s surname] [-n name] [-m misc-name] [--id id] [fullname]

Search and print a list of authors by surname/name/misc name/full name.

Options::

    -s, --surname surname       Search by surname
    -n, --name name             Search by name
    -m, --misc-name misc. name  Search by misc. name
    --id id                     Search by database id

Example::

    ml-search.py -i author -s duck

Search and print a list of authors whose surname starts with "duck",
case insensitive.

If a few options are given the search is limited with operator AND.
Example::

    ml-search.py -i author -s duck -n mack

Search and print a list of authors whose surname starts with "duck" and
name starts with "mack", case insensitive.

With one option `-v` it also prints database id.


Book search
^^^^^^^^^^^

Usage::

    ml-search.py books [-t title] [-s series] [-a archive] [-f file] [-p path] [--get] [--id id] [--surname name] [--name name] [--misc-name name] [--fullname name] [--aid aid] [-e ext] [--eid eid] [--gname name] [--gtitle title] [--gid gid] [-l lang] [--lid lid]

Search and print a list of books by title, series, archive or file name.

Options::

    -t, --title title      Search by title
    -s, --series series    Search by series
    -a, --archive archive  Search by archive (zip file)
    -f, --file file        Search by file name (without extension)
    -p, --path path        Path to the directory with the library
                           archives
    --get                  Download exactly one book
    --id id                Search by database id
    --surname surname      Search by author’s surname
    --name name            Search by author’s name
    --misc-name misc. name Search by author’s misc. name
    --fullname name        Search by author’s full name
    --aid aid              Search by author’s id
    -e, --ext ext          Search by file extension
    --eid eid              Search by extension’s id
    --gname name           Search by genre’s name
    --gtitle title         Search by genre’s title
    --gid gid              Search by genre’s id
    -l, --lang lang        Search by language
    --lid lid              Search by language’s id

By default the program prints only titles of the found book. With one
option `-v` it also prints database id, the list of authors and genres,
and also series the book belongs to (if any) and the serial number of
the book in the series. With two options `-v` (`-v -v` or simply `-vv`)
it also prints the file date and language. With three `-v` it prints
archive name, file name, extension and size, and flag if the book is
marked to be deleted.

Option `-p` provides the path to the directory with the library
archives. By default the path is extracted from `m_librarian.conf`,
section `[library]`, key `path`::

    [library]
    path = /var/lib/archives

The option is useful for multiple databases (global option `-d`).

Option `--get` allows to download a book from the library to a local
file. The option allows to download exactly one book. The simplest way
to use it is via option `--id`. The file is downloaded into the current
directory with the name from the library.


Extension search
^^^^^^^^^^^^^^^^

Usage::

    ml-search.py ext [name] [--id id]

Options::

    --id id                Search by database id

Search and print a list of extensions by name.

With one option `-v` it also prints database id.


Genres search
^^^^^^^^^^^^^

Usage::

    ml-search.py genres [-n name] [-t title] [--id id]

Search and print a list of genres by name and title.

Options::

    -n, --name name    Search by name
    -t, --title title  Search by title
    --id id            Search by database id

With one option `-v` it also prints database id.


Language search
^^^^^^^^^^^^^^^

Usage::

    ml-search.py lang [name] [--id id]

Search and print a list of languages by name.

Options::

    --id id                Search by database id

With one option `-v` it also prints database id.

.. vim: set tw=72 :
