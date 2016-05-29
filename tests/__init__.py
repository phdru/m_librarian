
import os
import unittest
from m_librarian.db import open_db, init_db
from m_librarian.inp import import_inpx

__all__ = ['TestCase', 'main']


class TestCase(unittest.TestCase):
    def setUp(self):
        try:
            os.remove('/tmp/m_librarian-test.sqlite')
        except OSError:
            pass
        open_db('sqlite:///tmp/m_librarian-test.sqlite')
        init_db()

    def tearDown(self):
        try:
            os.remove('/tmp/m_librarian-test.sqlite')
        except OSError:
            pass

    def import_inpx(self, inpx):
        import_inpx(os.path.join(os.path.dirname(__file__), inpx))


def main():
    try:
        unittest.main(testRunner=unittest.TextTestRunner())
    except SystemExit, msg:
        result = msg.args[0]
    else:
        result = 0
    raise SystemExit(result)
