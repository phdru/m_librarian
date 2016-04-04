#! /usr/bin/env python

from m_librarian.db import open_db, init_db
from m_librarian.glst import import_glst

if __name__ == '__main__':
    open_db()
    init_db()
    old, new = import_glst()
    if old:
        print "Imported %d genres (ignored %d existing)" % (new, old)
    else:
        print "Imported %d genres" % new
