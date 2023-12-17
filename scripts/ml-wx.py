#! /usr/bin/env python

import sys
from m_librarian.wx.Application import Application


def main():
    if len(sys.argv) > 1:
        sys.exit("This program doesn't accept any arguments")
    app = Application()
    app.MainLoop()


if __name__ == '__main__':
    main()
