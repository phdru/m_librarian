#! /usr/bin/env python

import os
from shutil import copyfileobj
from zipfile import ZipFile
from .config import get_config

__all__ = ['download']


_library_path = None


def download(archive, filename):
    global _library_path
    if _library_path is None:
        _library_path = get_config().get('library', 'path')

    zf = ZipFile(os.path.join(_library_path, archive),  'r')
    infile = zf.open(filename)
    outfile = open(filename, 'wb')
    copyfileobj(infile, outfile)
    outfile.close()
    infile.close()
    zf.close()
