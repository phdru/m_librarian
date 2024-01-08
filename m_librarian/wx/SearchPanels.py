# coding: utf-8

import wx
from ..config import get_config
from ..search import search_authors_raw, search_books_raw
from .ListAuthors import ListAuthorsWindow, ListBooksWindow


_search_types = ['start', 'substring', 'full']


class SearchPanel(wx.Panel):

    # Subclasses must override these
    search_title = None
    search_button_title = None

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        search_vsizer = \
            wx.StaticBoxSizer(wx.VERTICAL, self, self.search_title)
        self.SetSizer(search_vsizer)

        self.search = search = \
            wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        search_vsizer.Add(search, 0, wx.EXPAND, 0)
        search.Bind(wx.EVT_TEXT_ENTER, self.DoSearch)

        self.search_substr = search_substr = wx.RadioBox(
            self,
            choices=[
                u'Подстрока в начале',
                u'Подстрока',
                u'Точное совпадение',
            ],
            majorDimension=1, style=wx.RA_SPECIFY_ROWS
        )
        search_vsizer.Add(search_substr)

        self.search_case = search_case = wx.CheckBox(
            self, label=u'Различать прописные/строчные')
        search_vsizer.Add(search_case)

        search_button = wx.Button(self, label=self.search_button_title)
        search_vsizer.Add(search_button, 0, wx.ALIGN_CENTER, 0)
        search_button.Bind(wx.EVT_BUTTON, self.DoSearch)

    def DoSearch(self, event):
        search = self.search.GetValue()
        search_substr = _search_types[self.search_substr.GetSelection()]
        search_case = self.search_case.GetValue()
        if search_case is False:
            search_case = None
        self.realSearch(search, search_substr, search_case)


class SearchAuthorsPanel(SearchPanel):

    search_title = u'Поиск авторов'
    search_button_title = u'Искать авторов'

    def realSearch(self, value, search_substr, search_case):
        search_results = \
            search_authors_raw(value, search_substr, search_case)
        ListAuthorsWindow(self.Parent, search_results)


class SearchBooksPanel(SearchPanel):

    search_title = u'Поиск книг'
    search_button_title = u'Искать книги'

    def __init__(self, parent):
        SearchPanel.__init__(self, parent)
        self.use_filters = use_filters = wx.CheckBox(
            self, label=u'Использовать фильтры')
        use_filters_cfg = \
            get_config().getint('filters', 'use_in_search_forms', 1)
        use_filters.SetValue(use_filters_cfg)
        sizer = self.GetSizer()
        s_count = len(sizer.GetChildren())
        sizer.Insert(s_count-1, use_filters)  # Insert before the cutton

    def realSearch(self, value, search_substr, search_case):
        use_filters = self.use_filters.GetValue()
        search_results = \
            search_books_raw(value, search_substr, search_case, use_filters)
        ListBooksWindow(self.Parent, search_results)
