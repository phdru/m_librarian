
from pytest import raises
from dbutils import setup_module, teardown_module  # noqa
from dbutils import load_inpx
from m_librarian.db import Author, Book


def test_import_bad_inpx():
    raises(ValueError, load_inpx, 'bad.inpx')


def test_import_inpx():
    load_inpx('test.inpx')
    assert Author.select().count() == 5
    assert Book.select().count() == 5
