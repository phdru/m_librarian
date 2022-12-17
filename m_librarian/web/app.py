# -*- coding: utf-8 -*-

import os

from sqlobject.sqlbuilder import CONCAT
from bottle import cheetah_view, redirect, request, route, static_file

from m_librarian.config import get_config
from m_librarian.db import Author, Book
from m_librarian.download import download
from m_librarian.search import search_authors, search_books


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
    columns = get_config().getlist('columns', 'author', ['fullname'])
    return {
        'authors': list(authors),
        'search_authors': value,
        'search_type': search_type,
        'case_sensitive': case_sensitive,
        'columns': columns,
    }


@route('/books-by-author/<aid:int>/', method='GET')
@cheetah_view('list_books.tmpl')
def books_by_author(aid):
    use_filters = get_config().getint('filters', 'use_in_books_list', 1)
    columns = get_config().getlist('columns', 'book', ['title'])
    author = Author.get(aid)
    if use_filters:
        join_expressions = []
        join_expressions.append(Book.j.authors)
        join_expressions.append(Author.q.id == aid)
        books = search_books('full', None, {}, join_expressions,
                             orderBy=('series', 'ser_no', 'title', '-date'),
                             use_filters=use_filters)
    else:
        books = Book.select(
            Book.j.authors & (Author.q.id == aid),
            orderBy=['series', 'ser_no', 'title'],
        )

    return {
        'books_by_author': {author.fullname: list(books)},
        'columns': columns,
    }


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
    download_path = get_config().getpath('download', 'path')
    if books_ids:
        for bid in books_ids:
            book = Book.get(int(bid))
            download(book, download_path)
        return {
            'message': u'Книги сохранены.',
        }
    else:
        return {
            'message': u'Не выбрано книг для сохранения.',
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
    value = decode(value)
    search_type = request.forms.get('search_type')
    if not search_type:
        search_type = 'start'
    case_sensitive = request.forms.get('case_sensitive')
    if case_sensitive is None:
        case_sensitive = _guess_case_sensitivity(value)
    use_filters = request.forms.get('use_filters')
    books = search_books(search_type, case_sensitive, {'title': value}, None,
                         orderBy=('title',), use_filters=use_filters)
    books_by_authors = {}
    for book in books:
        author = book.author1
        if author in books_by_authors:
            books_by_author = books_by_authors[author]
        else:
            books_by_author = books_by_authors[author] = []
        books_by_author.append(book)
    columns = get_config().getlist('columns', 'book', ['title'])
    return {
        'books_by_author': books_by_authors,
        'search_books': value,
        'search_type': search_type,
        'case_sensitive': case_sensitive,
        'columns': columns,
    }
