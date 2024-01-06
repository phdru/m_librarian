# coding: utf-8

import wx
from .AWindow import AWindow


class ListBooksWindow(AWindow):

    session_config_section_name = 'list_books'
    window_title = u"m_Librarian: Список книг"

    def __init__(self, parent, author):
        self.author = author
        AWindow.__init__(self, parent)
