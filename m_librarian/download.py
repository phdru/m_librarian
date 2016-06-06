#! /usr/bin/env python

import os
from time import mktime
from shutil import copyfileobj
from zipfile import ZipFile
from .config import get_config

__all__ = ['download']


_format = '%f'
_compile_format = True
_compiled_format = '%(file)s'


def _do_compile_format():
    global _format, _compile_format, _compiled_format
    if _compile_format:
        _compile_format = False
        try:
            _format = get_config().get('download', 'format')
        except:
            return
    got_percent = False
    compiled = []
    for c in _format:
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
    _compiled_format = ''.join(compiled)


_library_path = None


def download(book, path=None):
    if path is None:
        global _library_path
        if _library_path is None:
            _library_path = get_config().get('library', 'path')
        path = _library_path

    global _compiled_format
    _do_compile_format()
    if _compiled_format[-1] in ('\0', '\\', '/'):
        raise ValueError('Bad format: "%s"' % _compiled_format)
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
    if '%(extension)s' not in _compiled_format:
        _compiled_format += '.%(extension)s'
    filename = _compiled_format % bdict
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError:
        pass  # Already exists
    zf = ZipFile(os.path.join(path, book.archive),  'r')
    infile = zf.open('%s.%s' % (book.file, book.extension.name))
    outfile = open(filename, 'wb')
    copyfileobj(infile, outfile)
    outfile.close()
    infile.close()
    zf.close()
    dt = mktime(book.date.timetuple())
    os.utime(filename, (dt, dt))


def test():
    _do_compile_format()
    print _compiled_format

if __name__ == '__main__':
    test()
