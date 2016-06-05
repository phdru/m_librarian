#! /usr/bin/env python

import os
from shutil import copyfileobj
from zipfile import ZipFile
from .config import get_config

__all__ = ['download']


_library_path = None


def download(archive, filename, path=None):
    if path is None:
        global _library_path
        if _library_path is None:
            _library_path = get_config().get('library', 'path')
        path = _library_path

    zf = ZipFile(os.path.join(path, archive),  'r')
    infile = zf.open(filename)
    outfile = open(filename, 'wb')
    copyfileobj(infile, outfile)
    outfile.close()
    infile.close()
    zf.close()
