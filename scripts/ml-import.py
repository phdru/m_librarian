#! /usr/bin/env python

import argparse
from m_librarian.config import get_config
from m_librarian.db import open_db, init_db, update_counters
from m_librarian.glst import import_glst
from m_librarian.inp import import_inpx

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import')
    parser.add_argument('-C', '--config', help='configuration file')
    parser.add_argument('-D', '--database', help='database URI')
    parser.add_argument('inpx', nargs='+', help='INPX files to import')
    args = parser.parse_args()

    if args.config:
        get_config(args.config)  # Get and cache config file

    open_db(args.database)
    init_db()
    import_glst()
    for inpx in args.inpx:
        import_inpx(inpx)
    update_counters()
