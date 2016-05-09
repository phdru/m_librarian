#! /usr/bin/env python

import argparse
import sys
from m_lib.defenc import default_encoding
from m_librarian.db import open_db
from m_librarian.search import search_authors
from m_librarian.translations import translations
_ = translations.ugettext


def _guess_case_sensitivity(values):
    for value in values.values():
        if not value.islower():
            return True
    return False


def _search_authors(case_sensitive, args):
    values = {}
    for column in 'surname', 'name', 'misc':
        value = getattr(args, column)
        if value:
            values[column] = unicode(value, default_encoding)
    if case_sensitive is None:
        case_sensitive = _guess_case_sensitivity(values)
    for author in search_authors(args.search_type, case_sensitive, values):
        full_name = filter(None,
                           (author.surname, author.name, author.misc_name))
        full_name = u' '.join(full_name)
        print full_name.encode(default_encoding), \
            (u"(%s: %d)" % (_('books'), author.count)).encode(default_encoding)


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
    parser.add_argument('-m', '--misc', help='search by misc. name')
    parser.set_defaults(func=_search_authors)

    args = main_parser.parse_args()
    if args.case_sensitive:
        if args.ignore_case:
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
