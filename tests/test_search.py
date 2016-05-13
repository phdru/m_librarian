#! /usr/bin/env python
# coding: utf-8


from tests import TestCase, main
from m_librarian.search import search_authors


class TestSearch(TestCase):
    def test_search_authors(self):
        self.import_inpx('test.inpx')
        self.assertEqual(
            search_authors('exact', True, {'surname': u'Друг'}).count(), 1)
        self.assertEqual(
            search_authors('start', True, {'surname': u'Друг'}).count(), 2)
        self.assertEqual(
            search_authors('substring', True, {'surname': u'Друг'}).count(), 2)
        self.assertEqual(
            search_authors('substring', False, {'surname': u'друг'}).count(),
            3)


if __name__ == "__main__":
    main()
