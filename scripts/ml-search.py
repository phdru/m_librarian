#! /usr/bin/env python

import argparse
import sys
from sqlobject.sqlbuilder import CONCAT

from m_lib.defenc import default_encoding
from m_librarian.db import Author, Book, Extension, Genre, Language, open_db
from m_librarian.download import download
from m_librarian.search import mk_search_conditions, \
    search_authors, search_books, \
    search_extensions, search_genres, search_languages

from m_librarian.translations import translations
_ = translations.ugettext


def _get_values(args, *columns):
    values = {}
    for column in columns:
        value = getattr(args, column)
        if value:
            if isinstance(value, basestring):
                value = unicode(value, default_encoding)
            values[column] = value
    return values


def _guess_case_sensitivity(values):
    for value in values.values():
        if isinstance(value, basestring) and not value.islower():
            return True
    return False


def print_count(count):
    print _("Found").encode(default_encoding), ":", count


def _search_authors(case_sensitive, search_type, args):
    if (args.surname or args.name or args.misc_name) and args.fullname:
        sys.stderr.write(
            "Cannot search by names and full name at the same time\n")
        main_parser.print_help()
        sys.exit(1)
    expressions = []
    values = _get_values(args, 'surname', 'name', 'misc_name', 'id')
    if not values:
        value = args.fullname
        if value:
            expressions.append((
                CONCAT(Author.q.surname, ' ', Author.q.name, ' ',
                       Author.q.misc_name),
                unicode(value, default_encoding)
            ))
    if case_sensitive is None:
        case_sensitive = _guess_case_sensitivity(values)
    authors = search_authors(search_type, case_sensitive, values, expressions,
                             orderBy=('surname', 'name', 'misc_name'))
    if args.count:
        print_count(authors.count())
        return
    count = 0
    for author in authors:
        print author.fullname.encode(default_encoding), \
            (u"(%s: %d)" % (_('books'), author.count))\
            .encode(default_encoding),
        if args.verbose >= 1:
            print "(id=%d)" % author.id,
        print
        count += 1
    print_count(count)


def _search_books(case_sensitive, search_type, args):
    if args.get and args.get_many:
        sys.stderr.write(
            "Cannot get one book and many books at the same time\n")
        main_parser.print_help()
        sys.exit(1)
    join_expressions = []
    values = _get_values(args, 'title', 'series', 'archive', 'file', 'id')
    if case_sensitive is None:
        test_values = values.copy()
        test_values.update(_get_values(args, 'surname', 'name', 'misc_name',
                                       'fullname', 'ext', 'gname', 'gtitle',
                                       'lang'))
        case_sensitive = _guess_case_sensitivity(test_values)
    avalues = _get_values(args, 'surname', 'name', 'misc_name', 'fullname')
    if args.aid:
        avalues['id'] = args.aid
    if avalues:
        if (args.surname or args.name or args.misc_name) and args.fullname:
            sys.stderr.write(
                "Cannot search by names and full name at the same time\n")
            main_parser.print_help()
            sys.exit(1)
        expressions = []
        join_expressions.append(Book.j.authors)
        value = args.fullname
        if value:
            expressions.append((
                CONCAT(Author.q.surname, ' ', Author.q.name, ' ',
                       Author.q.misc_name),
                unicode(value, default_encoding)
            ))
        conditions = mk_search_conditions(
            Author, search_type, case_sensitive, avalues, expressions)
        join_expressions.extend(conditions)
    evalues = {}
    if args.ext:
        evalues['name'] = args.ext
    if args.eid:
        evalues['id'] = args.eid
    if evalues:
        join_expressions.append(Book.j.extension)
        conditions = mk_search_conditions(
            Extension, search_type, case_sensitive, evalues)
        join_expressions.extend(conditions)
    gvalues = {}
    for column in 'name', 'title':
        value = getattr(args, 'g' + column)
        if value:
            gvalues[column] = unicode(value, default_encoding)
    if args.gid:
        gvalues['id'] = args.gid
    if gvalues:
        join_expressions.append(Book.j.genres)
        conditions = mk_search_conditions(
            Genre, search_type, case_sensitive, gvalues)
        join_expressions.extend(conditions)
    lvalues = {}
    if args.lang:
        lvalues['name'] = args.lang
    if args.lid:
        lvalues['id'] = args.lid
    if lvalues:
        join_expressions.append(Book.j.language)
        conditions = mk_search_conditions(
            Language, search_type, case_sensitive, lvalues)
        join_expressions.extend(conditions)
    books = search_books(search_type, case_sensitive, values, join_expressions,
                         orderBy=('series', 'ser_no', 'title'))
    if args.count:
        print_count(books.count())
        return
    if args.get_many:
        books = books[:args.get_many]
    elif args.get:
        count = books.count()
        if count != 1:
            sys.stderr.write("There must be exactly 1 book for --get; "
                             "(found %d).\n" % count)
            sys.stderr.write("Use --get-many N to download more than one "
                             "book.\n")
            sys.exit(1)
    count = 0
    for book in books:
        print book.title.encode(default_encoding),
        if args.verbose >= 1:
            print "(id=%d)" % book.id,
        print
        if args.verbose >= 1:
            print " ", _("Author(s)").encode(default_encoding), ":",
            for author in book.authors:
                print author.fullname.encode(default_encoding),
            print
            print " ", _("Genre(s)").encode(default_encoding), ":",
            for genre in book.genres:
                print (genre.title or genre.name).encode(default_encoding),
            print
            if book.series:
                print " ", _("Series").encode(default_encoding), ":",
                print book.series.encode(default_encoding), \
                    "(%d)" % book.ser_no

        if args.verbose >= 2:
            print " ", _("Date").encode(default_encoding), ":", book.date
            print " ", _("Language").encode(default_encoding), ":", \
                book.language.name.encode(default_encoding)

        if args.verbose >= 3:
            print " ", _("Archive").encode(default_encoding), ":", book.archive
            print " ", _("File").encode(default_encoding), ":", book.file
            print " ", _("Extension").encode(default_encoding), ":", \
                book.extension.name.encode(default_encoding)
            print " ", _("Size").encode(default_encoding), ":", \
                book.size, _("bytes").encode(default_encoding)
            print " ", _("Deleted").encode(default_encoding), ":", \
                _(str(book.deleted)).encode(default_encoding)
        if args.get or args.get_many:
            download(book, args.path, args.format)
        count += 1
    print_count(count)


def _search_extensions(case_sensitive, search_type, args):
    values = _get_values(args, 'name', 'id')
    if case_sensitive is None:
        case_sensitive = _guess_case_sensitivity(values)
    else:
        values = {}
    extensions = search_extensions(search_type, case_sensitive, values,
                                   orderBy='name')
    if args.count:
        print_count(extensions.count())
        return
    count = 0
    for ext in extensions:
        print ext.name.encode(default_encoding), \
            (u"(%s: %d)" % (_('books'), ext.count)).encode(default_encoding),
        if args.verbose >= 1:
            print "(id=%d)" % ext.id,
        print
        count += 1
    print_count(count)


def _search_genres(case_sensitive, search_type, args):
    values = _get_values(args, 'name', 'title', 'id')
    if case_sensitive is None:
        case_sensitive = _guess_case_sensitivity(values)
    genres = search_genres(search_type, case_sensitive, values, orderBy='name')
    if args.count:
        print_count(genres.count())
        return
    count = 0
    for genre in genres:
        names = filter(None, (genre.name, genre.title))
        fullname = u' '.join(names)
        print fullname.encode(default_encoding), \
            (u"(%s: %d)" % (_('books'), genre.count)).encode(default_encoding),
        if args.verbose >= 1:
            print "(id=%d)" % genre.id,
        print
        count += 1
    print_count(count)


def _search_languages(case_sensitive, search_type, args):
    values = _get_values(args, 'name', 'id')
    if case_sensitive is None:
        case_sensitive = _guess_case_sensitivity(values)
    else:
        values = {}
    languages = search_languages(search_type, case_sensitive, values,
                                 orderBy='name')
    if args.count:
        print_count(languages.count())
        return
    count = 0
    for lang in languages:
        print lang.name.encode(default_encoding), \
            (u"(%s: %d)" % (_('books'), lang.count)).encode(default_encoding),
        if args.verbose >= 1:
            print "(id=%d)" % lang.id,
        print
        count += 1
    print_count(count)


if __name__ == '__main__':
    main_parser = argparse.ArgumentParser(description='Search')
    main_parser.add_argument('-d', '--database', help='database URI')
    main_parser.add_argument('-i', '--ignore-case', action='store_true',
                             help='ignore case '
                             '(default is to guess)')
    main_parser.add_argument('-I', '--case-sensitive', action='store_true',
                             help='don\'t ignore case')
    main_parser.add_argument('-t', '--start', action='store_true',
                             help='search substring at the start '
                             '(this is the default)')
    main_parser.add_argument('-s', '--substring', action='store_true',
                             help='search substring anywhere')
    main_parser.add_argument('-f', '--full', action='store_true',
                             help='match the entire string')
    main_parser.add_argument('-c', '--count', action='store_true',
                             help='count instead of output')
    main_parser.add_argument('-v', '--verbose', action='count',
                             help='output more details about books; '
                             'repeat for even more details')
    subparsers = main_parser.add_subparsers(help='Commands')

    parser = subparsers.add_parser('authors', help='Search authors')
    parser.add_argument('-s', '--surname', help='search by surname')
    parser.add_argument('-n', '--name', help='search by name')
    parser.add_argument('-m', '--misc-name', help='search by misc. name')
    parser.add_argument('--id', type=int, help='search by database id')
    parser.add_argument('fullname', nargs='?', help='search by full name')
    parser.set_defaults(func=_search_authors)

    parser = subparsers.add_parser('books', help='Search books')
    parser.add_argument('-t', '--title', help='search by title')
    parser.add_argument('-s', '--series', help='search by series')
    parser.add_argument('-a', '--archive', help='search by archive (zip file)')
    parser.add_argument('-f', '--file', help='search by file name')
    parser.add_argument('-p', '--path', help='path to the library archives')
    parser.add_argument('--format', help='download format, default is %f')
    parser.add_argument('--get', action='store_true',
                        help='download exactly one book')
    parser.add_argument('--get-many', type=int,
                        help='download at most this many books')
    parser.add_argument('--id', type=int, help='search by database id')
    parser.add_argument('--surname', help='search by author\'s surname')
    parser.add_argument('--name', help='search by author\'s name')
    parser.add_argument('--misc-name', help='search by author\'s misc. name')
    parser.add_argument('--fullname', help='search by author\'s full name')
    parser.add_argument('--aid', type=int, help='search by author\'s id')
    parser.add_argument('-e', '--ext', help='search by file extension')
    parser.add_argument('--eid', type=int, help='search by extension\'s id')
    parser.add_argument('--gname', help='search by genre\'s name')
    parser.add_argument('--gtitle', help='search by genre\'s title')
    parser.add_argument('--gid', type=int, help='search by genre\'s id')
    parser.add_argument('-l', '--lang', help='search by language')
    parser.add_argument('--lid', type=int, help='search by language\'s id')
    parser.set_defaults(func=_search_books)

    parser = subparsers.add_parser('ext', help='Search extensions')
    parser.add_argument('name', nargs='?', help='search by name')
    parser.add_argument('--id', type=int, help='search by database id')
    parser.set_defaults(func=_search_extensions)

    parser = subparsers.add_parser('genres', help='Search genres')
    parser.add_argument('-n', '--name', help='search by name')
    parser.add_argument('-t', '--title', help='search by title')
    parser.add_argument('--id', type=int, help='search by database id')
    parser.set_defaults(func=_search_genres)

    parser = subparsers.add_parser('lang', help='Search languages')
    parser.add_argument('name', nargs='?', help='search by name')
    parser.add_argument('--id', type=int, help='search by database id')
    parser.set_defaults(func=_search_languages)

    args = main_parser.parse_args()

    if args.case_sensitive:
        if args.ignore_case:
            sys.stderr.write(
                "Cannot search case sensitive and case insensitive "
                "at the same time\n")
            main_parser.print_help()
            sys.exit(1)
        else:
            case_sensitive = True
    elif args.ignore_case:
        case_sensitive = False
    else:
        case_sensitive = None  # guess case sensitivity

    if int(args.start) + int(args.substring) + int(args.full) > 1:
        sys.stderr.write(
            "Cannot search case sensitive and case insensitive "
            "at the same time\n")
        main_parser.print_help()
        sys.exit(1)
    if args.start:
        search_type = 'start'
    elif args.substring:
        search_type = 'substring'
    elif args.full:
        search_type = 'full'
    else:
        search_type = 'start'

    open_db(args.database)
    args.func(case_sensitive, search_type, args)
