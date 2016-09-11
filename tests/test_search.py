# coding: utf-8

from tests import TestCase
from m_librarian.db import Author, Book
from m_librarian.search import mk_search_conditions, \
    search_authors, search_books


class TestSearch(TestCase):
    def test_search_authors(self):
        self.import_inpx('test.inpx')
        self.assertEqual(
            search_authors('full', True, {'surname': u'Друг'}).count(), 1)
        self.assertEqual(
            search_authors('start', True, {'surname': u'Друг'}).count(), 2)
        self.assertEqual(
            search_authors('substring', True, {'surname': u'Друг'}).count(), 2)
        self.assertEqual(
            search_authors('substring', False, {'surname': u'друг'}).count(),
            3)

        join_expressions = []
        join_expressions.append(Book.j.authors)
        conditions = mk_search_conditions(
            Author, 'start', False, {'surname': u'друг'})
        join_expressions.extend(conditions)
        self.assertEqual(
            search_books('start', False,
                         {'title': u'тест'}, join_expressions).count(),
            2)
