
import os
from zipfile import ZipFile
from sqlobject import sqlhub
from sqlobject.sqlbuilder import Select
from .db import Author, Book, Extension, Genre, Language, \
    insert_name, insert_author

__all__ = ['import_inpx']


EOT = chr(4)  # INP field separator


def split_line(line):
    parts = line.strip().split(EOT)
    _l = len(parts)
    if _l < 11:
        raise ValueError('Unknown INP structure: "%s"' % line)
    archive = None
    if _l == 11:  # Standard structure
        parts.append(None)  # Emulate lang
    elif _l == 15:  # New structure
        parts = parts[:12]
    elif _l == 17:  # Very new structure
        archive = parts[12]
        language = parts[13]
        parts = parts[:11] + [language]
    else:  # New structure
        raise ValueError('Unknown INP structure: "%s"' % line)
    return archive, parts


def import_inp_line(archive, parts):
    authors, genres, title, series, ser_no, file, size, lib_id, deleted, \
        extension, date, language = parts
    try:
        ser_no = int(ser_no)
    except ValueError:
        ser_no = None
    size = int(size)
    deleted = deleted == '1'
    extension_row = insert_name(Extension, extension)
    language_row = insert_name(Language, language)
    book = Book(title=title, series=series, ser_no=ser_no,
                archive=archive, file=file, size=size,
                lib_id=lib_id, deleted=deleted,
                extension=extension_row, date=date,
                language=language_row)
    authors = authors.split(':')
    seen_authors = set()
    for author in authors:
        if author:
            if author in seen_authors:
                continue
            seen_authors.add(author)
            alist = author.split(',', 2)
            surname = alist[0]
            if len(alist) > 1:
                name = alist[1]
                if len(alist) == 3:
                    misc_name = alist[2]
                else:
                    misc_name = ''
            else:
                name = misc_name = ''
            author_row = insert_author(surname, name, misc_name)
            book.addAuthor(author_row)
    for genre in genres.split(':'):
        if genre:
            genre_row = insert_name(Genre, genre, title=genre)
            book.addGenre(genre_row)


def tounicode(s):
    if isinstance(s, bytes):
        return s.decode('utf-8')
    else:
        return s


def import_inp(archive, inp):
    archives = set()
    files = set()
    connection = sqlhub.processConnection
    for file, in connection.queryAll(connection.sqlrepr(
            Select(Book.q.file, Book.q.archive == archive))):
        files.add((archive, tounicode(file)))
    for line in inp:
        line = line.decode('utf-8')
        _archive, parts = split_line(line)
        if _archive and (_archive not in archives):
            archives.add(_archive)
            for file, in connection.queryAll(connection.sqlrepr(
                    Select(Book.q.file, Book.q.archive == _archive))):
                files.add((_archive, tounicode(file)))
        file = parts[5]
        if (_archive or archive, file) not in files:
            files.add((_archive or archive, file))
            import_inp_line(_archive or archive, parts)


def import_inpx(path, pbar_cb=None):
    inpx = ZipFile(path)
    if pbar_cb:
        inp_count = 0
        for name in inpx.namelist():
            ext = os.path.splitext(name)[1]
            if ext == '.inp':
                inp_count += 1
        pbar_cb.set_max(inp_count)
    inp_count = 0
    for name in inpx.namelist():
        archive, ext = os.path.splitext(name)
        if ext != '.inp':
            continue
        if pbar_cb:
            inp_count += 1
            pbar_cb.display(inp_count)
        inp = inpx.open(name)
        sqlhub.doInTransaction(import_inp, archive + '.zip', inp)
        inp.close()
    connection = sqlhub.processConnection
    if connection.dbName == 'postgres':
        for table in Author, Book, Extension, Genre, Language:
            connection.query("VACUUM %s" % table.sqlmeta.table)
    elif connection.dbName == 'sqlite':
        connection.query("VACUUM")
    if pbar_cb:
        pbar_cb.close()
