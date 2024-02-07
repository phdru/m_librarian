# coding: utf-8

import wx, wx.grid  # noqa: E401 multiple imports on one line
from ..compat import string_type, unicode_type
from ..download import download
from ..translations import translations
from .Grids import GridWindow, GridPanel


_ = getattr(translations, 'ugettext', None) or translations.gettext


class BooksDataTable(wx.grid.GridTableBase):
    def __init__(self, rows_count, column_names):
        wx.grid.GridTableBase.__init__(self)
        self.rows_count = rows_count
        self.column_names = column_names
        self.data = []
        for row in range(rows_count + 1):
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
        grid.SetTable(
            BooksDataTable(total_rows+1, columns),
            takeOwnership=True,
        )
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
        grid.SetCellAlignment(row, 1, wx.ALIGN_CENTRE, wx. ALIGN_CENTRE)
        grid.SetCellSize(row, 1, 1, len(columns)-1)
        row = 1
        self.book_by_row = book_by_row = {}  # map {row: book}
        self.toggle_rows = toggle_rows = {}  # map {row: [list of subrows]}
        for author in sorted(books_by_author):
            grid.SetCellAlignment(row, 1, wx.ALIGN_LEFT, wx. ALIGN_CENTRE)
            grid.SetCellSize(row, 1, 1, len(columns)-1)
            grid.SetCellValue(row, 1, u'%s' % (author,))
            author_row = row
            toggle_rows[author_row] = []
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
                    series_row = row
                    toggle_rows[author_row].append(row)
                    toggle_rows[series_row] = []
                    row += 1
                    series = book.series
                for col, col_name in enumerate(columns[1:]):
                    value = getattr(book, col_name)
                    if value is None:
                        value = u''
                    elif not isinstance(value, (string_type, unicode_type)):
                        value = str(value)
                    grid.SetCellValue(row, col+1, value)
                book_by_row[row] = book
                toggle_rows[author_row].append(row)
                toggle_rows[series_row].append(row)
                row += 1
        toggle_rows[0] = [row_ for row_ in range(1, row)]
        grid.AutoSizeColumns()
        grid.AutoSizeRows()
        grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnClick)

        search_button = wx.Button(self, label=u'Скачать')
        self.GetSizer().Add(search_button, 0, wx.ALIGN_CENTER, 0)
        search_button.Bind(wx.EVT_BUTTON, self.Download)

    def toggleCB(self, row):
        value = self.grid.GetCellValue(row, 0)
        if value:
            value = ''
        else:
            value = '1'
        self.grid.SetCellValue(row, 0, value)
        toggle_rows = self.toggle_rows
        if row in toggle_rows:
            for row_ in toggle_rows[row]:
                self.grid.SetCellValue(row_, 0, value)

    def OnClick(self, event):
        if event.GetCol() > 0:
            return
        self.toggleCB(event.GetRow())

    def OnDClick(self, event):
        if event.GetCol() == 0:
            return
        self.toggleCB(event.GetRow())

    def OnKeyDown(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Parent.Close()
        else:
            event.Skip()

    def Download(self, event=None):
        book_by_row = self.book_by_row
        found_books = False
        try:
            for row in self.toggle_rows[0]:
                value = self.grid.GetCellValue(row, 0)
                if value and row in book_by_row:
                    found_books = True
                    download(book_by_row[row])
        except Exception as e:
            self.report_error(str(e))
        else:
            if not found_books:
                self.report_error(u'Не выбрано книг для сохранения.')

    def report_error(self, error):
        wx.MessageBox(
            error, caption='m_Librarian download error',
            style=wx.OK | wx.ICON_ERROR, parent=self.Parent)


class ListBooksWindow(GridWindow):

    session_config_section_name = 'list_books'
    window_title = u"m_Librarian: Список книг"
    GridPanelClass = ListBooksPanel

    def InitMenu(self):
        GridWindow.InitMenu(self)

        download_menu = wx.Menu()
        download = download_menu.Append(wx.ID_SAVE,
                                        u"&Скачать", u"Скачать")
        self.Bind(wx.EVT_MENU, self.OnDownload, download)
        self.GetMenuBar().Append(download_menu, u"&Скачать")

    def OnDownload(self, event):
        self.panel.Download()
