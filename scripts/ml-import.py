#! /usr/bin/env python
from __future__ import print_function

import argparse
import sys

from m_librarian.config import get_config
from m_librarian.db import open_db, init_db, update_counters
from m_librarian.glst import import_glst
from m_librarian.inp import import_inpx
from m_librarian.pbar import ttyProgressBar
if ttyProgressBar:
    from m_librarian.pbar import ml_ttyProgressBar

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import')
    parser.add_argument('-C', '--config', help='configuration file')
    parser.add_argument('-D', '--database', help='database URI')
    parser.add_argument('-P', '--no-pbar', action='store_true',
                        help='inhibit progress bar')
    parser.add_argument('inpx', nargs='+', help='INPX files to import')
    args = parser.parse_args()

    if args.config:
        get_config(args.config)  # Get and cache config file

    open_db(args.database)
    init_db()

    count_old, count_new = import_glst()
    if count_old:
        print("Imported %d genres (ignored %d existing)" % (
            count_new, count_old))
    else:
        print("Imported %d genres" % count_new)

    use_pbar = ttyProgressBar and not args.no_pbar and sys.stdout.isatty()
    for inpx in args.inpx:
        if use_pbar:
            if len(inpx) > 25:
                pbar_fname = inpx[:22] + '...'
            else:
                pbar_fname = inpx
            print(pbar_fname.ljust(20), end=': ')
            sys.stdout.flush()
            pbar = ml_ttyProgressBar()
            import_inpx(inpx, pbar_cb=pbar)
            print("Ok")
        else:
            import_inpx(inpx)
    if use_pbar:
        print("Updating counters", end=': ')
        sys.stdout.flush()
        pbar = ml_ttyProgressBar()
        update_counters(pbar_cb=pbar)
        print("Ok")
    else:
        update_counters()
