#! /usr/bin/env python

from m_librarian.db import init_db
from m_librarian.glst import import_data

if __name__ == '__main__':
    init_db()
    old, new = import_data()
    if old:
        print "Imported %d genres (ignored %d existing)" % (new, old)
    else:
        print "Imported %d genres" % new
