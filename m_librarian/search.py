from sqlobject.sqlbuilder import AND, OR, func
from .config import get_config
from .db import Author, Book, Extension, Genre, Language

__all__ = [
    'mk_search_conditions',
    'search_authors', 'search_books', 'search_extensions',
    'search_genres', 'search_languages',
]


def _mk_search_conditions_with_operator(table, case_sensitive, comparison_op,
                                        values, expressions):
    if expressions is None:
        expressions = []
    _expressions = []
    for column, value in values.items():
        if column == 'id':
            _expressions.append(table.q.id == value)
            break
    if case_sensitive:
        for column, value in values.items():
            if column == 'id':
                continue
            _expressions.append(
                getattr(getattr(table.q, column), comparison_op)(value))
        for expr, value in expressions:
            _expressions.append(
                getattr(expr, comparison_op)(value))
    else:
        for column, value in values.items():
            if column == 'id':
                continue
            _expressions.append(
                getattr(func.lower(
                    getattr(table.q, column)),
                    comparison_op)(value.lower()))
        for expr, value in expressions:
            _expressions.append(
                getattr(func.lower(expr), comparison_op)(value.lower()))
    return _expressions


_comparison_operators = {
    'start': 'startswith',
    'substring': 'contains',
    'full': '__eq__',
}


def mk_search_conditions(table, search_type, case_sensitive, values,
                         expressions=None, join_expressions=None):
    if join_expressions is None:
        join_expressions = []
    return _mk_search_conditions_with_operator(
        table, case_sensitive, _comparison_operators[search_type],
        values, expressions) + join_expressions


def _search(table, search_type, case_sensitive, values,
            expressions=None, join_expressions=None, orderBy=None):
    conditions = mk_search_conditions(
        table, search_type, case_sensitive, values, expressions=expressions,
        join_expressions=join_expressions)
    return table.select(AND(*conditions), orderBy=orderBy)


def search_authors(search_type, case_sensitive, values,
                   expressions=None, orderBy=None):
    return _search(Author, search_type, case_sensitive, values,
                   expressions=expressions, orderBy=orderBy)


def search_books(search_type, case_sensitive, values, join_expressions=None,
                 orderBy=None, use_filters=False):
    if use_filters:
        config = get_config()
        lang_filter = config.getlist('filters', 'lang')
        deleted_filter = config.getint('filters', 'deleted')
        if lang_filter:
            if join_expressions is None:
                join_expressions = []
            lang_conditions = []
            for lang in lang_filter:
                lvalues = {'name': lang}
                conditions = mk_search_conditions(
                    Language, search_type, case_sensitive, lvalues)
                lang_conditions.append(conditions)
            join_expressions.append(Book.j.language)
            join_expressions.append(OR(*lang_conditions))
    conditions = mk_search_conditions(
        Book, search_type, case_sensitive, values,
        join_expressions=join_expressions)
    if use_filters and not deleted_filter:
        conditions.append(Book.q.deleted == False)  # noqa: E712
    return Book.select(AND(*conditions), orderBy=orderBy)


def search_extensions(search_type, case_sensitive, values, orderBy=None):
    return _search(Extension, search_type, case_sensitive, values,
                   orderBy=orderBy)


def search_genres(search_type, case_sensitive, values, orderBy=None):
    return _search(Genre, search_type, case_sensitive, values,
                   orderBy=orderBy)


def search_languages(search_type, case_sensitive, values, orderBy=None):
    return _search(Language, search_type, case_sensitive, values,
                   orderBy=orderBy)
