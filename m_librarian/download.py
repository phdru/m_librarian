#! /usr/bin/env python

from __future__ import print_function
import os
from time import mktime
from shutil import copyfileobj
from zipfile import ZipFile
from .config import get_config

__all__ = ['download']


format = '%f'
compile_format = True
compiled_format = '%(file)s'


def _compile_format():
    global format, compile_format, compiled_format
    if compile_format:
        compile_format = False
        try:
            format = get_config().get('download', 'format')
        except Exception:
            return
    got_percent = False
    compiled = []
    for c in format:
        if c == '%':
            if got_percent:
                got_percent = False
                compiled.append('%')
            else:
                got_percent = True
        else:
            if got_percent:
                got_percent = False
                if c == 'a':
                    new_format = u'%(author)s'
                elif c == 'e':
                    new_format = u'%(extension)s'
                elif c == 'f':
                    new_format = u'%(file)s'
                elif c == 'G':
                    new_format = u'%(gname)s'
                elif c == 'g':
                    new_format = u'%(gtitle)s'
                elif c == 'l':
                    new_format = u'%(language)s'
                elif c == 'n':
                    new_format = u'%(ser_no)d'
                elif c == 's':
                    new_format = u'%(series)s'
                elif c == 't':
                    new_format = u'%(title)s'
                else:
                    raise ValueError('Bad format specifier "%%%c"' % c)
                compiled.append(new_format)
            else:
                compiled.append(c)
    compiled_format = ''.join(compiled)


_library_path = None


def download(book, dest_path=None, lib_path=None, a_format=None):
    if lib_path is None:
        global _library_path
        if _library_path is None:
            _library_path = get_config().get('library', 'path')
        lib_path = _library_path

    global format, compile_format, compiled_format
    if a_format:
        format = a_format
        compile_format = True
    _compile_format()
    if compiled_format[-1] in ('\0', '\\', '/'):
        raise ValueError('Bad format: "%s"' % compiled_format)
    bdict = {}
    bdict['author'] = book.authors[0].fullname
    bdict['extension'] = book.extension.name
    bdict['file'] = book.file
    genre = book.genres[0]
    bdict['gname'] = genre.name
    bdict['gtitle'] = genre.title
    bdict['language'] = book.language.name
    bdict['ser_no'] = book.ser_no or 0
    bdict['series'] = book.series
    bdict['title'] = book.title
    if '%(extension)s' not in compiled_format:
        compiled_format += '.%(extension)s'
    filename = compiled_format % bdict
    full_path = os.path.join(dest_path, filename)
    try:
        os.makedirs(os.path.dirname(full_path))
    except OSError:
        pass  # Already exists
    zf = ZipFile(os.path.join(lib_path, book.archive),  'r')
    infile = zf.open('%s.%s' % (book.file, book.extension.name))
    outfile = open(full_path, 'wb')
    copyfileobj(infile, outfile)
    outfile.close()
    infile.close()
    zf.close()
    dt = mktime(book.date.timetuple())
    os.utime(full_path, (dt, dt))


def test():
    _compile_format()
    print(compiled_format)


if __name__ == '__main__':
    test()
