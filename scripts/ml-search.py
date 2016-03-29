#! /usr/bin/env python
# coding: utf-8

import argparse
from m_lib.defenc import default_encoding
from m_librarian.search import search_authors, search_books, \
    search_extensions, search_genres, search_languages


def _search_authors(args):
    values = {}
    for column in 'surname', 'name', 'misc':
        value = getattr(args, column)
        if value:
            values[column] = unicode(value, default_encoding)
    for author in search_authors(args.search_type, args.case_sensitive,
                                 values):
        full_name = filter(None,
                           (author.surname, author.name, author.misc_name))
        full_name = u' '.join(full_name)
        print full_name.encode(default_encoding), \
            u"(книг: %d)".encode(default_encoding) % author.count


if __name__ == '__main__':
    main_parser = argparse.ArgumentParser(description='Search')
    main_parser.add_argument('-I', '--case-sensitive',
                             action='store_true',
                             help='don\'t ignore case '
                             '(default is case-insensitive search)')
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
    args.func(args)
