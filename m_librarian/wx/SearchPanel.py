# coding: utf-8

import wx


class SearchPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.search_authors_vsizer = search_authors_vsizer = \
            wx.StaticBoxSizer(wx.VERTICAL, self, u'Поиск авторов')
        self.SetSizer(search_authors_vsizer)

        self.search_authors = search_authors = \
            wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        search_authors_vsizer.Add(search_authors, 0, wx.EXPAND, 0)
        search_authors.Bind(wx.EVT_TEXT_ENTER, self.SearchAuthors)

        self.search_substr = search_substr = wx.RadioBox(
            self,
            choices=[
                u'Подстрока в начале',
                u'Подстрока',
                u'Точное совпадение',
            ],
            majorDimension=1, style=wx.RA_SPECIFY_ROWS
        )
        search_authors_vsizer.Add(search_substr)

        self.search_case = search_case = wx.CheckBox(
            self, label=u'Различать прописные/строчные')
        search_authors_vsizer.Add(search_case)

        self.search_authors_button = search_authors_button = wx.Button(
            self, label=u'Искать авторов')
        search_authors_vsizer.Add(search_authors_button, 0, wx.ALIGN_CENTER, 0)
        search_authors_button.Bind(wx.EVT_BUTTON, self.SearchAuthors)

    def SearchAuthors(self, event):
        pass
