
Before you begin
================

Before you begin you need some preparations.


.. contents::
   :local:


Software
--------

m_Librarian is written in Python and requires Python 2.7. So install
Python 2.7 first. Install required modules: SQLObject and m_lib.


Library archives
----------------

The program works with local library archives so download some. In
addition to the very libraries you need to get INPX indices for them —
m_Librarian cannot index libraries yet.


Database
--------

The program needs a database. It can work with any database supported by
SQLObject. Preferred ones are: MySQL, PostgreSQL or SQLite. If you plan
to use an SQL server you must create a database yourself. For SQLite,
the database file will be created by the program, so it's the simplest
way of using m_Librarian.

Database URI
^^^^^^^^^^^^

For m_Librarian to use an SQL server create a configuration file and put
it in $HOME/.config/ (if your OS is POSIX-compatible). Name the
configuration file ``m_librarian.conf``. It must be in ``ini``-file
format and must have the only section ``[database]`` with the only key
``URI``. The value for the key must be a Database URI in format accepted
by SQLObject. Some examples::

   [database]
   URI = mysql://user:password@host/database

   [database]
   URI = postgres://user@host/database

   [database]
   URI = sqlite:///full/path/to/database

See some more examples in sample/m_librarian.conf. See detailed
description for DB URIs in `SQLObject documentation
<http://sqlobject.org/SQLObject.html#declaring-a-connection>`_.

.. vim: set tw=72 :
