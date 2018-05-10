
from dbutils import setup_module, teardown_module  # noqa
from m_librarian.db import Genre
from m_librarian.glst import import_glst


def test_import_glst():
    import_glst()
    assert Genre.select().count() == 370
