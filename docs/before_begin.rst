
Before you begin
================

Before you begin you need some preparations.


.. contents::
   :local:

.. highlight:: none

Software
--------

m_Librarian is written in Python and requires Python (2.7 or 3.4+). So
install Python first. Install required modules: SQLObject and
m_lib.defenc. pip `installs <install.html>`_ required modules
automatically.


Library archives
----------------

The program works with local library archives so download some. In
addition to the very libraries you need to get INPX indices for them —
m_Librarian cannot index libraries yet.

Configuration file
------------------

m_librarian looks up configuration file in $HOME/.config/ (if your OS is
POSIX-compatible). The configuration file must be named
``m_librarian.conf``. It must be in ``ini``-file format. The following
sections and keys are now understood::

    [database]
    URI = "database URI"

    [library]
    path = "path to the library archives"

    [download]
    format = "download file format"

Most programs have an option `-C|--config file` to use a non-default
configuration file.

Database
--------

The program needs a database. It can work with any database supported by
SQLObject. Preferred ones are: MySQL, PostgreSQL or SQLite. If you plan
to use an SQL server you must create a database yourself. For SQLite,
the database file will be created by the program, so it's the simplest
way of using m_Librarian.

Database URI
^^^^^^^^^^^^

In configuration file define section ``[database]`` with the only key
``URI``. The value for the key must be a Database URI in format accepted
by SQLObject. Some examples::

   [database]
   URI = mysql://user:password@host/database

   [database]
   URI = postgres://user@host/database

   [database]
   URI = sqlite:///full/path/to/database

See some more examples in m_librarian.conf.sample. See detailed
description for DB URIs in `SQLObject documentation
<http://sqlobject.org/SQLObject.html#declaring-a-connection>`_.

.. vim: set tw=72 :
