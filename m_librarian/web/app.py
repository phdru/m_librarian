# -*- coding: utf-8 -*-

import os

from sqlobject.sqlbuilder import CONCAT
from bottle import cheetah_view, redirect, request, route, static_file

from m_librarian.config import get_config
from m_librarian.db import Author, Book
from m_librarian.download import download
from m_librarian.search import search_authors


@route('/')
@cheetah_view('index.tmpl')
def index():
    return {}


@route('/search_authors', method='GET')
def _search_authors():
    return redirect('/search_authors/')


@route('/search_authors/', method='GET')
@cheetah_view('search_authors.tmpl')
def search_authors_get():
    return {}


def decode(value):
    if isinstance(value, bytes):
        return value.decode('utf-8')
    return value


def _guess_case_sensitivity(value):
    return not value.islower()


@route('/search_authors/', method='POST')
@cheetah_view('list_authors.tmpl')
def search_authors_post():
    value = request.forms.get('search_authors')
    if not value:
        return redirect('/search_authors/')
    value = decode(value)
    search_type = request.forms.get('search_type')
    if not search_type:
        search_type = 'start'
    case_sensitive = request.forms.get('case_sensitive')
    if case_sensitive is None:
        case_sensitive = _guess_case_sensitivity(value)
    expressions = [(
        CONCAT(Author.q.surname, ' ', Author.q.name, ' ', Author.q.misc_name),
        decode(value)
    )]
    authors = search_authors(search_type, case_sensitive, {}, expressions,
                             orderBy=('surname', 'name', 'misc_name'))
    return {
        'authors': list(authors),
        'search_authors': value,
        'search_type': search_type,
        'case_sensitive': case_sensitive,
    }


@route('/books-by-author/<id:int>/', method='GET')
@cheetah_view('books_by_author.tmpl')
def books_by_author(id):
    return {
        'author': Author.get(id),
        'books': Book.select(
            Book.j.authors & (Author.q.id == id),
            orderBy=['series', 'ser_no', 'title'],
        )
    }


@route('/static/<filename:path>')
def send_static(filename):
    return static_file(
        filename, root=os.path.join(
            os.path.dirname(__file__),
            'static'
        )
    )


@route('/download/<id:int>/', method='GET')
@cheetah_view('download.tmpl')
def download_book(id):
    book = Book.get(id)
    download(book, get_config().get('download', 'path'))
    return {
        'message': u'Книга сохранена',
    }
