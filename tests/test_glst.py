
from tests import TestCase
from m_librarian.db import Genre
from m_librarian.glst import import_glst


class TestGlst(TestCase):
    def test_import_glst(self):
        import_glst()
        self.assertEqual(Genre.select().count(), 340)
