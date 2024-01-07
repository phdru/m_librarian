# coding: utf-8

import wx
from ..compat import string_type, unicode_type
from ..translations import translations
from .Grids import GridWindow, GridPanel


class ListBooksPanel(GridPanel):

    def InitGrid(self):
        _ = getattr(translations, 'ugettext', None) or translations.gettext
        books_by_author = self.param['books_by_author']
        columns = self.param['columns']
        author = next(iter(books_by_author))
        books = books_by_author[author]
        series = {book.series for book in books}
        grid = self.grid
        grid.CreateGrid(len(books) + len(series), len(columns))
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
        row = 0
        series = None
        for book in books:
            if book.series != series:
                if book.series:
                    value = book.series
                else:
                    value = u'Вне серий'
                grid.SetCellAlignment(row, 0, wx.ALIGN_LEFT, wx. ALIGN_CENTRE)
                grid.SetCellSize(row, 0, 1, len(columns))
                grid.SetCellValue(row, 0, u'%s — %s' % (book.author1, value))
                row += 1
                series = book.series
            for col, col_name in enumerate(columns):
                value = getattr(book, col_name)
                if value is None:
                    value = u''
                elif not isinstance(value, (string_type, unicode_type)):
                    value = str(value)
                grid.SetCellValue(row, col, value)
            row += 1
        grid.AutoSizeColumns()
        grid.AutoSizeRows()

    def OnDClick(self, event):
        pass

    def OnKeyDown(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Parent.Close()
        else:
            event.Skip()

class ListBooksWindow(GridWindow):

    session_config_section_name = 'list_books'
    window_title = u"m_Librarian: Список книг"
    GridPanelClass = ListBooksPanel
