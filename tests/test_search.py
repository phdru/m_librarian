# coding: utf-8

from dbutils import setup_module, teardown_module  # noqa
from dbutils import load_inpx
from m_librarian.db import Author, Book
from m_librarian.search import mk_search_conditions, \
    search_authors, search_books


def test_search_authors():
    load_inpx('test.inpx')
    assert search_authors('full', True, {'surname': u'Друг'}).count() == 1
    assert search_authors('start', True, {'surname': u'Друг'}).count() == 2
    assert search_authors('substring', True, {'surname': u'Друг'}).count() == 2
    assert search_authors(
        'substring', False, {'surname': u'друг'}).count() == 3

    join_expressions = []
    join_expressions.append(Book.j.authors)
    conditions = mk_search_conditions(
        Author, 'start', False, {'surname': u'друг'})
    join_expressions.extend(conditions)
    assert search_books(
        'start', False, {'title': u'тест'}, join_expressions).count() == 2
