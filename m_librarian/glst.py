#! /usr/bin/env python

from __future__ import print_function
import codecs
from glob import glob
import os
from sqlobject import sqlhub, SQLObjectNotFound
from .db import Genre

__all__ = ['import_glst']


def parse_glst_file(glst_filename):
    glst_file = codecs.open(glst_filename, 'r', 'utf-8')
    try:
        for line in glst_file:
            line = line.strip()
            if not line:
                continue
            if line[0] == '#':
                continue
            parts = line.split(None, 1)
            try:
                name, title = parts[1].split(';', 1)
            except (IndexError, ValueError):
                continue
            yield name, title
    finally:
        glst_file.close()


def import_glst_file(glst_filename):
    old = new = 0
    for name, title in parse_glst_file(glst_filename):
        try:
            Genre.byName(name)
        except SQLObjectNotFound:
            Genre(name=name, title=title, count=0)
            new += 1
        else:
            old += 1
    return old, new


def _import_glst():
    ml_dir = os.path.dirname(__file__)
    count_old = count_new = 0
    for glst_file in glob(os.path.join(ml_dir, 'glst', '*.glst')):
        _count_old, _count_new = import_glst_file(glst_file)
        count_old += _count_old
        count_new += _count_new
    connection = sqlhub.processConnection
    if connection.dbName == 'postgres':
        connection.query("VACUUM %s" % Genre.sqlmeta.table)
    return count_old, count_new


def import_glst():
    count_old, count_new = sqlhub.doInTransaction(_import_glst)
    connection = sqlhub.processConnection
    if connection.dbName == 'sqlite':
        connection.query("VACUUM")
    return count_old, count_new


def test():
    ml_dir = os.path.dirname(__file__)
    for i, (name, title) in enumerate(parse_glst_file(
        os.path.join(ml_dir, 'glst', 'genres_fb2_flibusta.glst')
    )):
        if i < 5:
            print(name, title)
        else:
            break


if __name__ == '__main__':
    test()
