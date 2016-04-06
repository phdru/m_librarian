#! /usr/bin/env python


import os
from tests import TestCase, main
from m_librarian.db import Author, Book
from m_librarian.inp import import_inpx


class TestInp(TestCase):
    def test_import_bad_inpx(self):
        self.assertRaises(
            ValueError, import_inpx,
            os.path.join(os.path.dirname(__file__), 'bad.inpx'))

    def test_import_inpx(self):
        import_inpx(os.path.join(os.path.dirname(__file__), 'test.inpx'))
        self.assertEqual(Author.select().count(), 4)
        self.assertEqual(Book.select().count(), 4)


if __name__ == "__main__":
    main()
