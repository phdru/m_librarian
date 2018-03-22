
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
    if _l == 11:  # Standard structure
        parts.append(None)  # Emulate lang
    else:  # New structure
        parts = parts[:12]
    return parts


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


def import_inp(archive, inp):
    files = set()
    connection = sqlhub.processConnection
    for file, in connection.queryAll(connection.sqlrepr(
            Select(Book.q.file, Book.q.archive == archive))):
        files.add(file)
    for line in inp:
        line = line.decode('utf-8')
        parts = split_line(line)
        file = parts[5]
        if file not in files:
            files.add(file)
            import_inp_line(archive, parts)


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
