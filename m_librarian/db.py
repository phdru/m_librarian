#! /usr/bin/env python

import os
from sqlobject import SQLObject, StringCol, UnicodeCol, IntCol, BoolCol, \
    ForeignKey, DateCol, DatabaseIndex, RelatedJoin, \
    connectionForURI, sqlhub, SQLObjectNotFound, dberrors
from .config import get_config

__all__ = ['Author', 'Book', 'Extension', 'Genre', 'Language',
           'AuthorBook', 'BookGenre', 'open_db', 'init_db',
           'insert_name', 'insert_author', 'update_counters',
           ]


class Author(SQLObject):
    surname = UnicodeCol(notNull=True)
    name = UnicodeCol(notNull=True)
    misc_name = UnicodeCol(notNull=True)
    count = IntCol(notNull=True)
    books = RelatedJoin('Book', otherColumn='book_id',
                        intermediateTable='author_book',
                        createRelatedTable=False)
    full_name_idx = DatabaseIndex(surname, name, misc_name, unique=True)
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
    title = UnicodeCol(notNull=True)
    series = UnicodeCol(notNull=True)
    ser_no = IntCol()
    archive = StringCol(notNull=True)
    file = StringCol(notNull=True)
    size = IntCol(notNull=True)
    lib_id = StringCol(notNull=True)
    deleted = BoolCol(notNull=True)
    extension = ForeignKey('Extension', notNull=True)
    date = DateCol(notNull=True)
    language = ForeignKey('Language')
    title_idx = DatabaseIndex(title)
    series_idx = DatabaseIndex(series)
    ser_no_idx = DatabaseIndex(ser_no)
    archive_idx = DatabaseIndex(archive)
    archive_file_idx = DatabaseIndex(archive, file, unique=True)
    file_idx = DatabaseIndex(file)
    size_idx = DatabaseIndex(size)
    deleted_idx = DatabaseIndex(deleted)
    extension_idx = DatabaseIndex(extension)
    date_idx = DatabaseIndex(date)
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
    name = UnicodeCol(notNull=True, unique=True)
    count = IntCol(notNull=True)
    count_idx = DatabaseIndex(count)


class Genre(SQLObject):
    name = UnicodeCol(notNull=True, unique=True)
    title = UnicodeCol(notNull=True)
    count = IntCol(notNull=True)
    books = RelatedJoin('Book', otherColumn='book_id',
                        intermediateTable='book_genre',
                        createRelatedTable=False)
    title_idx = DatabaseIndex(title)
    count_idx = DatabaseIndex(count)


class Language(SQLObject):
    name = UnicodeCol(notNull=True, unique=True)
    count = IntCol(notNull=True)
    count_idx = DatabaseIndex(count)


def _find_sqlite_db_dirs_posix():
    db_dirs = []
    if 'XDG_CACHE_HOME' in os.environ:
        db_dirs.append(os.environ['XDG_CACHE_HOME'])
    home_cache = os.path.expanduser('~/.cache')
    if home_cache not in db_dirs:
        db_dirs.append(home_cache)
    return db_dirs


def find_sqlite_db_dirs():
    if os.name == 'posix':
        return _find_sqlite_db_dirs_posix()
    raise OSError("Unknow OS")


def find_sqlite_dburi(db_dirs=None):
    if db_dirs is None:
        db_dirs = find_sqlite_db_dirs()
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

    return 'sqlite://%s' % db_file.replace(os.sep, '/')


def open_db(db_uri=None):
    if db_uri is None:
        try:
            db_uri = get_config().get('database', 'URI')
        except:
            db_uri = find_sqlite_dburi()

    if '://' not in db_uri:
        db_uri = 'sqlite://' + os.path.abspath(db_uri).replace(os.sep, '/')

    sqlhub.processConnection = connection = connectionForURI(db_uri)

    if connection.dbName == 'sqlite':
        def lower(s):
            if isinstance(s, basestring):
                return s.lower()
            return s

        sqlite = connection.module

        class MLConnection(sqlite.Connection):
            def __init__(self, *args, **kwargs):
                super(MLConnection, self).__init__(*args, **kwargs)
                self.create_function('lower', 1, lower)

        # This hack must be done at the very beginning, before the first query
        connection._connOptions['factory'] = MLConnection

        # Speedup SQLite connection
        connection.query("PRAGMA synchronous=OFF")
        connection.query("PRAGMA count_changes=OFF")
        connection.query("PRAGMA journal_mode=MEMORY")
        connection.query("PRAGMA temp_store=MEMORY")


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


def insert_author(surname, name, misc_name):
    try:
        return Author.full_name_idx.get(
            surname=surname, name=name, misc_name=misc_name)
    except SQLObjectNotFound:
        return Author(surname=surname, name=name, misc_name=misc_name, count=0)


def update_counters():
    for author in Author.select():
        author.count = AuthorBook.select(AuthorBook.q.author == author).count()

    for ext in Extension.select():
        ext.count = Book.select(Book.q.extension == ext.id).count()

    for genre in Genre.select():
        genre.count = BookGenre.select(BookGenre.q.genre == genre).count()

    for language in Language.select():
        language.count = Book.select(Book.q.language == language.id).count()


def test():
    db_dirs = find_sqlite_db_dirs()
    print "DB dirs:", db_dirs
    print "DB URI:", find_sqlite_dburi()

if __name__ == '__main__':
    test()
