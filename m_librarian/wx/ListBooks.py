# coding: utf-8

import wx, wx.grid  # noqa: E401 multiple imports on one line
from ..compat import string_type, unicode_type
from ..translations import translations
from .Grids import GridWindow, GridPanel


_ = getattr(translations, 'ugettext', None) or translations.gettext


class BooksDataTable(wx.grid.GridTableBase):
    def __init__(self, rows_count, column_names):
        wx.grid.GridTableBase.__init__(self)
        self.rows_count = rows_count
        self.column_names = column_names
        self.data = []
        for row in range(rows_count):
            row_data = []
            self.data.append(row_data)
            for col in range(len(column_names)):
                row_data.append('')

    # required methods for the wxPyGridTableBase interface

    def GetNumberRows(self):
        return self.rows_count

    def GetNumberCols(self):
        return len(self.column_names)

    def IsEmptyCell(self, row, col):
        return False

    # Get/Set values in the table.  The Python version of these
    # methods can handle any data-type, (as long as the Editor and
    # Renderer understands the type too,) not just strings as in the
    # C++ version.
    def GetValue(self, row, col):
        return self.data[row][col]

    def SetValue(self, row, col, value):
        self.data[row][col] = value

    # Optional methods

    # Called when the grid needs to display labels
    def GetRowLabelValue(self, row):
        return str(row)

    def GetColLabelValue(self, col):
        return _(self.column_names[col])

    # Called to determine the kind of editor/renderer to use by
    # default, doesn't necessarily have to be the same type used
    # natively by the editor/renderer if they know how to convert.
    def GetTypeName(self, row, col):
        if col == 0:
            return wx.grid.GRID_VALUE_BOOL
        else:
            return wx.grid.GRID_VALUE_STRING

    # Called to determine how the data can be fetched and stored by the
    # editor and renderer.  This allows you to enforce some type-safety
    # in the grid.
    def CanGetValueAs(self, row, col, typeName):
        colType = self.GetTypeName(row, col)
        if typeName == colType:
            return True
        else:
            return False

    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)


class ListBooksPanel(GridPanel):

    def InitGrid(self):
        books_by_author = self.param['books_by_author']
        columns = self.param['columns']
        columns.insert(0, u'Выбрать')
        total_rows = 0
        for author in books_by_author:
            books = books_by_author[author]
            series = {book.series for book in books}
            total_rows += len(books) + len(series) + 1
        grid = self.grid
        grid.SetTable(BooksDataTable(total_rows, columns), takeOwnership=True)
        grid.EnableEditing(False)
        for col, col_name in enumerate(columns):
            grid.AutoSizeColLabelSize(col)
            if col == 0:
                cell_attr = wx.grid.GridCellAttr()
                cell_attr.SetAlignment(wx.ALIGN_CENTRE, wx. ALIGN_CENTRE)
                grid.SetColAttr(col, cell_attr)
            elif col_name in ('ser_no', 'size'):
                cell_attr = wx.grid.GridCellAttr()
                cell_attr.SetAlignment(wx.ALIGN_RIGHT, wx. ALIGN_CENTRE)
                grid.SetColAttr(col, cell_attr)
        row = 0
        for author in sorted(books_by_author):
            grid.SetCellAlignment(row, 1, wx.ALIGN_LEFT, wx. ALIGN_CENTRE)
            grid.SetCellSize(row, 1, 1, len(columns)-1)
            grid.SetCellValue(row, 1, u'%s' % (author,))
            row += 1
            books = books_by_author[author]
            series = None
            for book in books:
                if book.series != series:
                    if book.series:
                        value = book.series
                    else:
                        value = u'Вне серий'
                    grid.SetCellAlignment(row, 1,
                                          wx.ALIGN_LEFT, wx. ALIGN_CENTRE)
                    grid.SetCellSize(row, 1, 1, len(columns)-1)
                    grid.SetCellValue(row, 1,
                                      u'%s — %s' % (book.author1, value))
                    row += 1
                    series = book.series
                for col, col_name in enumerate(columns[1:]):
                    value = getattr(book, col_name)
                    if value is None:
                        value = u''
                    elif not isinstance(value, (string_type, unicode_type)):
                        value = str(value)
                    grid.SetCellValue(row, col+1, value)
                row += 1
        grid.AutoSizeColumns()
        grid.AutoSizeRows()
        grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnClick)

    def toggleCB(self, row):
        value = self.grid.GetCellValue(row, 0)
        if value:
            value = ''
        else:
            value = '1'
        self.grid.SetCellValue(row, 0, value)

    def OnClick(self, event):
        if event.GetCol() > 0:
            return
        row = event.GetRow()
        self.toggleCB(row)

    def OnDClick(self, event):
        if event.GetCol() == 0:
            return
        row = event.GetRow()
        self.toggleCB(row)

    def OnKeyDown(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Parent.Close()
        else:
            event.Skip()


class ListBooksWindow(GridWindow):

    session_config_section_name = 'list_books'
    window_title = u"m_Librarian: Список книг"
    GridPanelClass = ListBooksPanel
