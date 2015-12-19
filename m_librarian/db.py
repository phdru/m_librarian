#! /usr/bin/env python

import os
from sqlobject import SQLObject, StringCol, UnicodeCol, IntCol, \
    connectionForURI, sqlhub
from .config import ml_conf

try:
    db_uri = ml_conf.get('database', 'URI')
except:
    db_uri = None

db_dirs = []
if not db_uri:
    if 'XDG_CACHE_HOME' in os.environ:
        db_dirs.append(os.environ['XDG_CACHE_HOME'])
    home_cache = os.path.expanduser('~/.cache')
    if home_cache not in db_dirs:
        db_dirs.append(home_cache)

    for d in db_dirs:
        db_file = os.path.join(d, 'm_librarian.sqlite')
        if os.path.exists(db_file):
            break
    else:
        # octal; -rw-------;
        # make the database file/directory readable/writeable only by the user
        os.umask(0066)
        db_dir = db_dirs[0]
        try:
            os.makedirs(db_dir)
        except OSError:  # Perhaps already exists
            pass
        db_file = os.path.join(db_dir, 'm_librarian.sqlite')
        db_uri = 'sqlite://%s' % db_file.replace(os.sep, '/')

sqlhub.processConnection = connectionForURI(db_uri)


class Author(SQLObject):
    name = UnicodeCol()
    count = IntCol()


class Book(SQLObject):
    name = UnicodeCol()


class Extension(SQLObject):
    name = StringCol()
    count = IntCol()


class Language(SQLObject):
    name = StringCol()
    count = IntCol()


if __name__ == '__main__':
    print "DB dirs:", db_dirs
    if db_uri:
        print "DB URI:", db_uri
