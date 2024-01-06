# coding: utf-8

import wx, wx.grid  # noqa: E401 multiple imports on one line
from ..compat import string_type, unicode_type
from ..translations import translations
from .AWindow import AWindow
from .ListBooks import ListBooksWindow


class ListAuthorsWindow(AWindow):

    session_config_section_name = 'list_authors'
    window_title = u"m_Librarian: Список авторов"

    def __init__(self, parent, search_authors_results):
        self.search_authors_results = search_authors_results
        AWindow.__init__(self, parent)

    def OnInit(self):
        AWindow.OnInit(self)
        ListAuthorsPanel(self, self.search_authors_results)


class ListAuthorsPanel(wx.Panel):

    def __init__(self, parent, search_authors_results):
        wx.Panel.__init__(self, parent)
        self.search_authors_results = search_authors_results

        list_authors_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(list_authors_sizer)

        self.grid = grid = wx.grid.Grid(self)
        list_authors_sizer.Add(grid, 0, wx.EXPAND, 0)

        self.InitGrid()

    def InitGrid(self):
        _ = getattr(translations, 'ugettext', None) or translations.gettext
        authors = self.search_authors_results['authors']
        columns = self.search_authors_results['columns']
        grid = self.grid
        grid.CreateGrid(len(authors), len(columns))
        grid.EnableEditing(False)
        for row in range(len(authors)):
            grid.SetRowLabelValue(row, str(row))
            grid.AutoSizeRowLabelSize(row)
        for col, col_name in enumerate(columns):
            grid.SetColLabelValue(col, _(col_name))
            grid.AutoSizeColLabelSize(col)
            if col_name == 'count':
                cell_attr = wx.grid.GridCellAttr()
                cell_attr.SetAlignment(wx.ALIGN_RIGHT, wx. ALIGN_CENTRE)
                grid.SetColAttr(col, cell_attr)
        for row, author in enumerate(authors):
            for col, col_name in enumerate(columns):
                value = getattr(author, col_name)
                if not isinstance(value, (string_type, unicode_type)):
                    value = str(value)
                grid.SetCellValue(row, col, value)
        grid.AutoSizeColumns()
        grid.AutoSizeRows()

        grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.OnDClick)
        grid.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

    def listBooks(self, row):
        authors = self.search_authors_results['authors']
        author = authors[row]
        ListBooksWindow(self, author)

    def OnDClick(self, event):
        row = event.GetRow()
        self.listBooks(row)

    def OnKeyDown(self, event):
        if event.GetKeyCode() in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            row = self.grid.GetGridCursorRow()
            self.listBooks(row)
        else:
            event.Skip()
