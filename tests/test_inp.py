
from tests import TestCase
from m_librarian.db import Author, Book


class TestInp(TestCase):
    def test_import_bad_inpx(self):
        self.assertRaises(ValueError, self.import_inpx, 'bad.inpx')

    def test_import_inpx(self):
        self.import_inpx('test.inpx')
        self.assertEqual(Author.select().count(), 4)
        self.assertEqual(Book.select().count(), 4)
