#! /usr/bin/env python

__all__ = ['Author', 'Book', 'Extension', 'Genre', 'Language',
           'init_db', 'insert_name',
           ]

import os
from sqlobject import SQLObject, StringCol, UnicodeCol, IntCol, BoolCol, \
    ForeignKey, DateCol, RelatedJoin, \
    connectionForURI, sqlhub, SQLObjectNotFound, dberrors
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
    name = UnicodeCol(unique=True)
    count = IntCol()
    books = RelatedJoin('Book', otherColumn='book_id')


class Book(SQLObject):
    authors = RelatedJoin('Author')
    genres = RelatedJoin('Genre')
    title = UnicodeCol()
    series = UnicodeCol()
    ser_no = IntCol()
    archive = StringCol()
    file = StringCol()
    size = IntCol()
    lib_id = StringCol()
    deleted = BoolCol()
    extension = ForeignKey('Extension')
    date = DateCol()
    language = ForeignKey('Language')


class Extension(SQLObject):
    name = StringCol(unique=True)
    count = IntCol()


class Genre(SQLObject):
    name = StringCol(unique=True)
    title = UnicodeCol()
    count = IntCol()
    books = RelatedJoin('Book', otherColumn='book_id')


class Language(SQLObject):
    name = StringCol(unique=True)
    count = IntCol()


def init_db():
    try:
        Book.select()[0]
    except IndexError:  # Table exists but is empty
        return
    except dberrors.Error:
        for table in Author, Extension, Genre, Language, Book:
            table.createTable()
    else:
        return


def insert_name(table, name):
    try:
        return table.byName(name)
    except SQLObjectNotFound:
        return table(name=name, count=0)


def test():
    print "DB dirs:", db_dirs
    if db_uri:
        print "DB URI:", db_uri

if __name__ == '__main__':
    test()
