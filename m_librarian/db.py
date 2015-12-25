#! /usr/bin/env python

__all__ = ['Author', 'Book', 'Extension', 'Genre', 'Language',
           'AuthorBook', 'BookGenre',
           'init_db', 'insert_name', 'update_counters',
           ]

import os
from sqlobject import SQLObject, StringCol, UnicodeCol, IntCol, BoolCol, \
    ForeignKey, DateCol, DatabaseIndex, RelatedJoin, \
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


sqlhub.processConnection = connection = connectionForURI(db_uri)

if connection.dbName == 'sqlite':
    # Speedup SQLite connection
    connection.query("PRAGMA synchronous=OFF")
    connection.query("PRAGMA count_changes=OFF")
    connection.query("PRAGMA journal_mode=MEMORY")
    connection.query("PRAGMA temp_store=MEMORY")


class Author(SQLObject):
    name = UnicodeCol(unique=True)
    count = IntCol()
    books = RelatedJoin('Book', otherColumn='book_id',
                        intermediateTable='author_book',
                        createRelatedTable=False)
    count_idx = DatabaseIndex(count)


class AuthorBook(SQLObject):
    class sqlmeta:
        table = "author_book"
    author = ForeignKey('Author', notNull=True, cascade=True)
    book = ForeignKey('Book', notNull=True, cascade=True)
    author_idx = DatabaseIndex(author)
    book_idx = DatabaseIndex(book)
    main_idx = DatabaseIndex(author, book, unique=True)


class Book(SQLObject):
    authors = RelatedJoin('Author',
                          intermediateTable='author_book',
                          createRelatedTable=False)
    genres = RelatedJoin('Genre',
                         intermediateTable='book_genre',
                         createRelatedTable=False)
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
    title_idx = DatabaseIndex(title)
    series_idx = DatabaseIndex(series)
    archive_file_idx = DatabaseIndex(archive, file, unique=True)
    extension_idx = DatabaseIndex(extension)
    language_idx = DatabaseIndex(language)


class BookGenre(SQLObject):
    class sqlmeta:
        table = "book_genre"
    book = ForeignKey('Book', notNull=True, cascade=True)
    genre = ForeignKey('Genre', notNull=True, cascade=True)
    book_idx = DatabaseIndex(book)
    genre_idx = DatabaseIndex(genre)
    main_idx = DatabaseIndex(book, genre, unique=True)


class Extension(SQLObject):
    name = StringCol(unique=True)
    count = IntCol()
    count_idx = DatabaseIndex(count)


class Genre(SQLObject):
    name = StringCol(unique=True)
    title = UnicodeCol()
    count = IntCol()
    books = RelatedJoin('Book', otherColumn='book_id',
                        intermediateTable='book_genre',
                        createRelatedTable=False)
    title_idx = DatabaseIndex(title)
    count_idx = DatabaseIndex(count)


class Language(SQLObject):
    name = StringCol(unique=True)
    count = IntCol()
    count_idx = DatabaseIndex(count)


def init_db():
    try:
        Book.select()[0]
    except IndexError:  # Table exists but is empty
        return
    except dberrors.Error:
        for table in Author, Extension, Genre, Language, Book, \
                AuthorBook, BookGenre:
            table.createTable()
    else:
        return


def insert_name(table, name, **kw):
    try:
        return table.byName(name)
    except SQLObjectNotFound:
        return table(name=name, count=0, **kw)


def update_counters():
    for author in Author.select():
        author.count = len(author.books)

    for ext in Extension.select():
        ext.count = Book.select(Book.q.extension == ext.name).count()

    for genre in Genre.select():
        genre.count = len(genre.books)

    for language in Language.select():
        language.count = Book.select(Book.q.language == language.name).count()


def test():
    print "DB dirs:", db_dirs
    if db_uri:
        print "DB URI:", db_uri

if __name__ == '__main__':
    test()
