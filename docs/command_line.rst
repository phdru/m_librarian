
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

Initialize database, import genres list and import a list of INPX files
listed in the command line. On subsequent runs doesn't destroy DB or
reimport genres; it also skips already import books but import new ones.

.. vim: set tw=72 :
