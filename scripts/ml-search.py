#! /usr/bin/env python

import argparse
import sys
from sqlobject.sqlbuilder import CONCAT

from m_lib.defenc import default_encoding
from m_librarian.db import Author, open_db
from m_librarian.search import search_authors, search_books, \
    search_extensions, search_genres, search_languages

from m_librarian.translations import translations
_ = translations.ugettext


def _guess_case_sensitivity(values):
    for value in values.values():
        if not value.islower():
            return True
    return False


def _search_authors(case_sensitive, args):
    if (args.surname or args.name or args.misc_name) and args.fullname:
        sys.stderr.write(
            "Cannot search by names and full name at the same time\n")
        main_parser.print_help()
        sys.exit(1)
    values = {}
    expressions = []
    for column in 'surname', 'name', 'misc_name':
        value = getattr(args, column)
        if value:
            values[column] = unicode(value, default_encoding)
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
    for author in search_authors(args.search_type, case_sensitive, values,
                                 expressions,
                                 orderBy=('surname', 'name', 'misc_name')):
        names = filter(None, (author.surname, author.name, author.misc_name))
        fullname = u' '.join(names)
        print fullname.encode(default_encoding), \
            (u"(%s: %d)" % (_('books'), author.count)).encode(default_encoding)


def _search_books(case_sensitive, args):
    values = {}
    for column in 'title', 'series', 'archive', 'file':
        value = getattr(args, column)
        if value:
            values[column] = unicode(value, default_encoding)
    if case_sensitive is None:
        case_sensitive = _guess_case_sensitivity(values)
    for book in search_books(args.search_type, case_sensitive, values,
                             orderBy='title'):
        print book.title.encode(default_encoding)
        for author in book.authors:
            names = filter(None,
                           (author.surname, author.name, author.misc_name))
            fullname = u' '.join(names)
            print fullname.encode(default_encoding),
        print


def _search_extensions(case_sensitive, args):
    if args.name:
        values = {'name': args.name}
        if case_sensitive is None:
            case_sensitive = _guess_case_sensitivity(values)
    else:
        values = {}
    for ext in search_extensions(args.search_type, case_sensitive, values,
                                 orderBy='name'):
        print ext.name.encode(default_encoding), \
            (u"(%s: %d)" % (_('books'), ext.count)).encode(default_encoding)


def _search_genres(case_sensitive, args):
    values = {}
    for column in 'name', 'title':
        value = getattr(args, column)
        if value:
            values[column] = unicode(value, default_encoding)
    if case_sensitive is None:
        case_sensitive = _guess_case_sensitivity(values)
    for genre in search_genres(args.search_type, case_sensitive, values,
                               orderBy='name'):
        names = filter(None, (genre.name, genre.title))
        fullname = u' '.join(names)
        print fullname.encode(default_encoding), \
            (u"(%s: %d)" % (_('books'), genre.count)).encode(default_encoding)


def _search_languages(case_sensitive, args):
    if args.name:
        values = {'name': args.name}
        if case_sensitive is None:
            case_sensitive = _guess_case_sensitivity(values)
    else:
        values = {}
    for lang in search_languages(args.search_type, case_sensitive, values,
                                 orderBy='name'):
        print lang.name.encode(default_encoding), \
            (u"(%s: %d)" % (_('books'), lang.count)).encode(default_encoding)


if __name__ == '__main__':
    main_parser = argparse.ArgumentParser(description='Search')
    main_parser.add_argument('-i', '--ignore-case',
                             action='store_true',
                             help='ignore case '
                             '(default is to guess)')
    main_parser.add_argument('-I', '--case-sensitive',
                             action='store_true',
                             help='don\'t ignore case ')
    main_parser.add_argument('-t', '--search-type',
                             choices=['exact', 'start', 'substring'],
                             default='start',
                             help='search type: '
                             'exact match, substring at the start '
                             '(this is the default), substring anywhere')
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
    open_db()
    args.func(case_sensitive, args)
