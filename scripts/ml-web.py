#! /usr/bin/env python

import argparse
import time
import webbrowser

from bottle import thread  # portable import

from m_librarian.db import open_db
import m_librarian.web.app  # noqa: F401 imported but unused
from m_librarian.web.server import run_server
from m_librarian.web.utils import get_lock, close_lock, get_open_port


def start_browser(port):
    time.sleep(1)  # A small timeout to allow the main thread to run the server
    webbrowser.open_new('http://localhost:%d/' % port)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Init')
    parser.add_argument('-p', '--port', help='HTTP server port')
    args = parser.parse_args()

    if args.port:
        port = args.port
    else:
        port = get_open_port()

    lock_file, old_port = get_lock(port)
    if lock_file:
        open_db()
        thread.start_new_thread(start_browser, (port,))
        run_server(port=port)
        close_lock(lock_file)
    else:  # Another instance of the program is being run at a different port
        start_browser(old_port)
