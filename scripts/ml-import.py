#! /usr/bin/env python

import argparse
from m_librarian.db import open_db, init_db, update_counters
from m_librarian.glst import import_glst
from m_librarian.inp import import_inpx

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import')
    parser.add_argument('-D', '--database', help='database URI')
    parser.add_argument('inpx', nargs='+', help='INPX files to import')
    args = parser.parse_args()

    open_db(args.database)
    init_db()
    import_glst()
    for inpx in args.inpx:
        import_inpx(inpx)
    update_counters()
