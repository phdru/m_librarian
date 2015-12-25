#! /usr/bin/env python

__all__ = ['import_glst']

import codecs
import os
from sqlobject import sqlhub, SQLObjectNotFound
from .db import Genre


def parse_glst_file(glst_filename):
    glst_file = codecs.open(glst_filename, 'r', 'utf-8')
    genre_list = []
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
            genre_list.append((name, title))
    finally:
        glst_file.close()
    return genre_list


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
    old_fb2, new_fb2 = import_glst_file(
        os.path.join(ml_dir, 'glst', 'genres_fb2.glst'))
    old_nonfb2, new_nonfb2 = import_glst_file(
        os.path.join(ml_dir, 'glst', 'genres_nonfb2.glst'))
    connection = sqlhub.processConnection
    if connection.dbName in ('postgres', 'sqlite'):
        connection.query("VACUUM %s" % Genre.sqlmeta.table)
    return old_fb2 + old_nonfb2, new_fb2 + new_nonfb2


def import_glst():
    return sqlhub.doInTransaction(_import_glst)


def test():
    ml_dir = os.path.dirname(__file__)
    print parse_glst_file(os.path.join(ml_dir, 'glst', 'genres_fb2.glst'))

if __name__ == '__main__':
    test()
