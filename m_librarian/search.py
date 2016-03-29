
__all__ = [
    'search_authors', 'search_books', 'search_extensions',
    'search_genres', 'search_languages',
]

from sqlobject.sqlbuilder import AND, func
from .db import Author, Book, Extension, Genre, Language


def _search_with_operator(table, case_sensitive, comparison_op, values):
    expressions = []
    if case_sensitive:
        for column, value in values.items():
            expressions.append(
                getattr(getattr(table.q, column), comparison_op)(value))
    else:
        for column, value in values.items():
            expressions.append(
                getattr(func.lower(
                    getattr(table.q, column)), comparison_op)(value.lower()))
    return AND(*expressions)


def _search_exact(table, case_sensitive, values):
    return _search_with_operator(table, case_sensitive, '__eq__', values)


def _search_start(table, case_sensitive, values):
    return _search_with_operator(table, case_sensitive, 'startswith', values)


def _search_substring(table, case_sensitive, values):
    return _search_with_operator(table, case_sensitive, 'contains', values)


def _search(table, search_type, case_sensitive, values):
    _search_f = globals()['_search_%s' % search_type]
    conditions = _search_f(table, case_sensitive, values)
    return table.select(conditions)


def search_authors(search_type, case_sensitive, values):
    return _search(Author, search_type, case_sensitive, values)


def search_books(search_type, case_sensitive, values):
    return _search(Book, search_type, case_sensitive, values)


def search_extensions(search_type, case_sensitive, values):
    return _search(Extension, search_type, case_sensitive, values)


def search_genres(search_type, case_sensitive, values):
    return _search(Genre, search_type, case_sensitive, values)


def search_languages(search_type, case_sensitive, values):
    return _search(Language, search_type, case_sensitive, values)
