# coding: utf-8

import wx, wx.grid  # noqa: E401 multiple imports on one line
from ..compat import string_type, unicode_type
from ..search import books_by_author
from ..translations import translations
from .Grids import GridWindow, GridPanel
from .ListBooks import ListBooksWindow


class ListAuthorsPanel(GridPanel):

    def InitGrid(self):
        _ = getattr(translations, 'ugettext', None) or translations.gettext
        authors = self.param['authors']
        columns = self.param['columns']
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

    def listBooks(self, row):
        authors = self.param['authors']
        author = authors[row]
        _books_by_author = books_by_author(author.id)
        ListBooksWindow(self, _books_by_author)

    def OnDClick(self, event):
        row = event.GetRow()
        self.listBooks(row)

    def OnKeyDown(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Parent.Close()
        elif event.GetKeyCode() in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            row = self.grid.GetGridCursorRow()
            self.listBooks(row)
        else:
            event.Skip()


class ListAuthorsWindow(GridWindow):

    session_config_section_name = 'list_authors'
    window_title = u"m_Librarian: Список авторов"
    GridPanelClass = ListAuthorsPanel
