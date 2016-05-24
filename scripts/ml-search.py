#! /usr/bin/env python

import argparse
import sys
from sqlobject.sqlbuilder import CONCAT

from m_lib.defenc import default_encoding
from m_librarian.db import Author, Book, Extension, Genre, Language, open_db
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
            values[column] = unicode(value, default_encoding)
    return values


def _guess_case_sensitivity(values):
    for value in values.values():
        if not value.islower():
            return True
    return False


def _search_authors(case_sensitive, search_type, args):
    if (args.surname or args.name or args.misc_name) and args.fullname:
        sys.stderr.write(
            "Cannot search by names and full name at the same time\n")
        main_parser.print_help()
        sys.exit(1)
    expressions = []
    values = _get_values(args, 'surname', 'name', 'misc_name')
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
    for author in search_authors(search_type, case_sensitive, values,
                                 expressions,
                                 orderBy=('surname', 'name', 'misc_name')):
        names = filter(None, (author.surname, author.name, author.misc_name))
        fullname = u' '.join(names)
        print fullname.encode(default_encoding), \
            (u"(%s: %d)" % (_('books'), author.count)).encode(default_encoding)


def _search_books(case_sensitive, search_type, args):
    join_expressions = []
    values = _get_values(args, 'title', 'series', 'archive', 'file')
    if case_sensitive is None:
        test_values = values.copy()
        test_values.update(_get_values(args, 'surname', 'name', 'misc_name',
                                       'fullname', 'ext', 'gname', 'gtitle',
                                       'lang'))
        case_sensitive = _guess_case_sensitivity(test_values)
    avalues = _get_values(args, 'surname', 'name', 'misc_name', 'fullname')
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
    if args.ext:
        join_expressions.append(Book.j.extension)
        conditions = mk_search_conditions(
            Extension, search_type, case_sensitive,
            {'name': args.ext})
        join_expressions.extend(conditions)
    gvalues = {}
    for column in 'name', 'title':
        value = getattr(args, 'g' + column)
        if value:
            gvalues[column] = unicode(value, default_encoding)
    if gvalues:
        join_expressions.append(Book.j.genres)
        conditions = mk_search_conditions(
            Genre, search_type, case_sensitive, gvalues)
        join_expressions.extend(conditions)
    if args.lang:
        join_expressions.append(Book.j.language)
        conditions = mk_search_conditions(
            Language, search_type, case_sensitive,
            {'name': args.lang})
        join_expressions.extend(conditions)
    for book in search_books(search_type, case_sensitive, values,
                             join_expressions,
                             orderBy=('series', 'ser_no', 'title')):
        print book.title.encode(default_encoding)
        if args.details >= 1:
            print " ", _("Author(s)"), ":",
            for author in book.authors:
                names = filter(None,
                               (author.surname, author.name, author.misc_name))
                fullname = u' '.join(names)
                print fullname.encode(default_encoding),
            print
            print " ", _("Genre(s)"), ":",
            for genre in book.genres:
                print (genre.title or genre.name).encode(default_encoding),
            print
            if book.series:
                print " ", _("Series"), ":",
                print book.series.encode(default_encoding), \
                    "(%d)" % book.ser_no

        if args.details >= 2:
            print " ", _("Date"), ":", book.date
            print " ", _("Language"), ":", book.language.name

        if args.details >= 3:
            print " ", _("Archive"), ":", book.archive
            print " ", _("File"), ":", book.file
            print " ", _("Extension"), ":", book.extension.name
            print " ", _("Size"), ":", book.size, _("bytes")
            print " ", _("Deleted"), ":", _(str(book.deleted))


def _search_extensions(case_sensitive, search_type, args):
    if args.name:
        values = {'name': args.name}
        if case_sensitive is None:
            case_sensitive = _guess_case_sensitivity(values)
    else:
        values = {}
    for ext in search_extensions(search_type, case_sensitive, values,
                                 orderBy='name'):
        print ext.name.encode(default_encoding), \
            (u"(%s: %d)" % (_('books'), ext.count)).encode(default_encoding)


def _search_genres(case_sensitive, search_type, args):
    values = _get_values(args, 'name', 'title')
    if case_sensitive is None:
        case_sensitive = _guess_case_sensitivity(values)
    for genre in search_genres(search_type, case_sensitive, values,
                               orderBy='name'):
        names = filter(None, (genre.name, genre.title))
        fullname = u' '.join(names)
        print fullname.encode(default_encoding), \
            (u"(%s: %d)" % (_('books'), genre.count)).encode(default_encoding)


def _search_languages(case_sensitive, search_type, args):
    if args.name:
        values = {'name': args.name}
        if case_sensitive is None:
            case_sensitive = _guess_case_sensitivity(values)
    else:
        values = {}
    for lang in search_languages(search_type, case_sensitive, values,
                                 orderBy='name'):
        print lang.name.encode(default_encoding), \
            (u"(%s: %d)" % (_('books'), lang.count)).encode(default_encoding)


if __name__ == '__main__':
    main_parser = argparse.ArgumentParser(description='Search')
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
    subparsers = main_parser.add_subparsers(help='Commands')

    parser = subparsers.add_parser('authors', help='Search authors')
    parser.add_argument('-s', '--surname', help='search by surname')
    parser.add_argument('-n', '--name', help='search by name')
    parser.add_argument('-m', '--misc-name', help='search by misc. name')
    parser.add_argument('fullname', nargs='?', help='search by full name')
    parser.set_defaults(func=_search_authors)

    parser = subparsers.add_parser('books', help='Search books')
    parser.add_argument('-t', '--title', help='search by title')
    parser.add_argument('-s', '--series', help='search by series')
    parser.add_argument('-a', '--archive', help='search by archive (zip file)')
    parser.add_argument('-f', '--file', help='search by file name')
    parser.add_argument('-d', '--details', action='count',
                        help='output more details about books; '
                        'repeat for even more details')
    parser.add_argument('--surname', help='search by author\'s surname')
    parser.add_argument('--name', help='search by author\'s name')
    parser.add_argument('--misc-name', help='search by author\'s misc. name')
    parser.add_argument('--fullname', help='search by author\'s full name')
    parser.add_argument('-e', '--ext', help='search by file extension')
    parser.add_argument('--gname', help='search by genre\'s name')
    parser.add_argument('--gtitle', help='search by genre\'s title')
    parser.add_argument('-l', '--lang', help='search by language')
    parser.set_defaults(func=_search_books)

    parser = subparsers.add_parser('ext', help='Search extensions')
    parser.add_argument('name', nargs='?', help='search by name')
    parser.set_defaults(func=_search_extensions)

    parser = subparsers.add_parser('genres', help='Search genres')
    parser.add_argument('-n', '--name', help='search by name')
    parser.add_argument('-t', '--title', help='search by title')
    parser.set_defaults(func=_search_genres)

    parser = subparsers.add_parser('lang', help='Search languages')
    parser.add_argument('name', nargs='?', help='search by name')
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

    open_db()
    args.func(case_sensitive, search_type, args)
