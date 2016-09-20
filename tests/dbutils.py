
import os
from m_librarian.db import open_db, init_db
from m_librarian.inp import import_inpx

__all__ = ['setup_module', 'teardown_module', 'load_inpx']


def setup_module():
    try:
        os.remove('/tmp/m_librarian-test.sqlite')
    except OSError:
        pass
    open_db('sqlite:///tmp/m_librarian-test.sqlite')
    init_db()


def teardown_module():
    try:
        os.remove('/tmp/m_librarian-test.sqlite')
    except OSError:
        pass


def load_inpx(inpx):
    import_inpx(os.path.join(os.path.dirname(__file__), inpx))
