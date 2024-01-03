# coding: utf-8

import wx


class SearchPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.search_authors_vsizer = search_authors_vsizer = \
            wx.StaticBoxSizer(wx.VERTICAL, self, u'Поиск авторов')
        self.SetSizer(search_authors_vsizer)

        self.search_authors = search_authors = wx.TextCtrl(self)
        search_authors_vsizer.Add(search_authors, 0, wx.EXPAND, 0)

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
