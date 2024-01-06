# coding: utf-8

import wx
from ..compat import string_type, unicode_type
from ..translations import translations
from .AWindow import AWindow


class ListBooksWindow(AWindow):

    session_config_section_name = 'list_books'
    window_title = u"m_Librarian: Список книг"

    def __init__(self, parent, books_by_author):
        self.books_by_author = books_by_author
        AWindow.__init__(self, parent)

    def OnInit(self):
        AWindow.OnInit(self)
        ListBooksPanel(self, self.books_by_author)


class ListBooksPanel(wx.Panel):

    def __init__(self, parent, books_by_author):
        wx.Panel.__init__(self, parent)
        self.books_by_author = books_by_author

        list_books_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(list_books_sizer)

        self.grid = grid = wx.grid.Grid(self)
        list_books_sizer.Add(grid, 0, wx.EXPAND, 0)

        self.InitGrid()

    def InitGrid(self):
        _ = getattr(translations, 'ugettext', None) or translations.gettext
        books_by_author = self.books_by_author['books_by_author']
        columns = self.books_by_author['columns']
        author = next(iter(books_by_author))
        books = books_by_author[author]
        grid = self.grid
        grid.CreateGrid(len(books), len(columns))
        grid.EnableEditing(False)
        for row in range(len(books)):
            grid.SetRowLabelValue(row, str(row))
            grid.AutoSizeRowLabelSize(row)
        for col, col_name in enumerate(columns):
            grid.SetColLabelValue(col, _(col_name))
            grid.AutoSizeColLabelSize(col)
            if col_name in ('ser_no', 'size'):
                cell_attr = wx.grid.GridCellAttr()
                cell_attr.SetAlignment(wx.ALIGN_RIGHT, wx. ALIGN_CENTRE)
                grid.SetColAttr(col, cell_attr)
        for row, book in enumerate(books):
            for col, col_name in enumerate(columns):
                value = getattr(book, col_name)
                if value is None:
                    value = u''
                elif not isinstance(value, (string_type, unicode_type)):
                    value = str(value)
                grid.SetCellValue(row, col, value)
        grid.AutoSizeColumns()
        grid.AutoSizeRows()
