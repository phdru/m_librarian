# -*- coding: utf-8 -*-

import os
from bottle import cheetah_view, redirect, request, route, static_file

from ..config import get_config
from ..db import Book
from ..download import download
from ..search import search_authors_raw, books_by_author, search_books_raw


@route('/')
@cheetah_view('index.tmpl')
def index():
    return {
        'get_config': get_config,
    }


@route('/search_authors', method='GET')
def _search_authors():
    return redirect('/search_authors/')


@route('/search_authors/', method='GET')
@cheetah_view('search_authors.tmpl')
def search_authors_get():
    return {}


@route('/list_authors', method='GET')
def _list_authors():
    return redirect('/list_authors/')


@route('/list_authors/', method='GET')
@cheetah_view('list_authors.tmpl')
def list_authors_get():
    value = request.query.get('search_authors')
    if not value:
        return redirect('/search_authors/')
    search_type = request.query.get('search_type')
    case_sensitive = request.query.get('case_sensitive')
    sort = request.query.get('sort')
    return search_authors_raw(value, search_type, case_sensitive, sort)


@route('/list_authors/', method='POST')
@cheetah_view('list_authors.tmpl')
def list_authors_post():
    value = request.forms.get('search_authors')
    if not value:
        return redirect('/search_authors/')
    search_type = request.forms.get('search_type')
    case_sensitive = request.forms.get('case_sensitive')
    sort = request.forms.get('sort')
    return search_authors_raw(value, search_type, case_sensitive, sort)


@route('/books-by-author/<aid:int>/', method='GET')
@cheetah_view('list_books.tmpl')
def _books_by_author(aid):
    return books_by_author(aid)


@route('/static/<filename:path>')
def send_static(filename):
    return static_file(
        filename, root=os.path.join(
            os.path.dirname(__file__),
            'static'
        )
    )


@route('/download/', method='POST')
@cheetah_view('download.tmpl')
def download_books():
    books_ids = []
    form = request.forms
    for k in form:
        if k.split('_')[-1] == 'books':
            for bid in form.getall(k):
                books_ids.append(bid)
    if books_ids:
        try:
            for bid in books_ids:
                book = Book.get(int(bid))
                download(book)
        except Exception as e:
            return {
                'error': str(e),
            }
        else:
            return {
                'message': u'Книги сохранены.',
            }
    else:
        return {
            'error': u'Не выбрано книг для сохранения.',
        }


@route('/search_books', method='GET')
def _search_books():
    return redirect('/search_books/')


@route('/search_books/', method='GET')
@cheetah_view('search_books.tmpl')
def search_books_get():
    return {
        'get_config': get_config,
    }


@route('/search_books/', method='POST')
@cheetah_view('list_books.tmpl')
def search_books_post():
    value = request.forms.get('search_books')
    if not value:
        return redirect('/search_books/')
    search_type = request.forms.get('search_type')
    case_sensitive = request.forms.get('case_sensitive')
    use_filters = request.forms.get('use_filters')
    return search_books_raw(value, search_type, case_sensitive, use_filters)
