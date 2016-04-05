
__all__ = ['TestCase', 'main']


import os
import unittest
from m_librarian.db import open_db, init_db


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


def main():
    try:
        unittest.main(testRunner=unittest.TextTestRunner())
    except SystemExit, msg:
        result = msg.args[0]
    else:
        result = 0
    raise SystemExit(result)
