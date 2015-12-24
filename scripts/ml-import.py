#! /usr/bin/env python

import sys
from m_librarian.db import init_db, update_counters
from m_librarian.glst import import_data
from m_librarian.inp import import_inpx

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Usage: %s file.inpx" % sys.argv[0])
    init_db()
    import_data()
    import_inpx(sys.argv[1])
    update_counters()
