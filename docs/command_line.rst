
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

    ml-search.py [-i] [-I] [-t {exact,start,substring}] ...

Search through the database and display results. Currently can only
search authors by name.

Global options::

    -i, --ignore-case     ignore case (default is to guess)
    -I, --case-sensitive  don't ignore case
    -t, --search-type {exact,start,substring}
        search type: exact match, substring at the start (this is the default),
        substring anywhere.

Options ``-i/-I`` cannot be used together as they are the opposite. In
case none of them are used the program guesses case-sensitivity by
looking at the arguments. If all arguments are lowercase the program
performs case-insensitive search. If there are UPPERCASE or MixedCase
arguments the program performs case-sensitive search.

Option ``-t/--search-type`` defines the search type. Search types are:

* exact - search for exact match; i.e. searching for "duck" returns
  results for "duck" but not for "duckling";
* start - search for substring at the start of the search field; for
  example searching for "duck" returns results for "duck" and "duckling"
  but not for "McDuck"; this is the default search type.
* substring - search for any substring; "duck" => "duck", "duckling",
  "McDuck" (except for case-sensitive search, of course).


Author search
^^^^^^^^^^^^^

Usage::

    ml-search.py [-i] [-I] [-t ...] author [-s surname] [-n name] [-m misc]

Search and print a list of authors by surname/name/misc name.

Options::

    -s, --surname surname  Search by surname
    -n, --name name        Search by name
    -m, --misc misc. name  Search by misc. name

Example::

    ml-search.py -i author -s duck

Search and print a list of authors whose surname starts with "duck",
case insensitive.

If a few options are given the search is limited with operator AND.
Example::

    ml-search.py -i author -s duck -n mack

Search and print a list of authors whose surname starts with "duck", and
name starts with "mack", case insensitive.

.. vim: set tw=72 :
