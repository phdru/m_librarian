
import os
from sqlobject.tests.dbtest import getConnection
from m_librarian.db import open_db, init_db
from m_librarian.inp import import_inpx

__all__ = ['setup_module', 'teardown_module', 'load_inpx']


def setup_module():
    connection = getConnection()
    if connection.dbName == 'sqlite':
        try:
            connection.dropDatabase()
        except OSError:
            pass
    open_db(connection.uri())
    init_db()


def teardown_module():
    connection = getConnection()
    if connection.dbName == 'sqlite':
        try:
            connection.dropDatabase()
        except OSError:
            pass


def load_inpx(inpx):
    import_inpx(os.path.join(os.path.dirname(__file__), inpx))
