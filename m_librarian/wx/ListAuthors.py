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
        self.param['column_sort'] = []
        grid = self.grid
        grid.CreateGrid(len(authors), len(columns))
        grid.EnableEditing(False)
        for row in range(len(authors)):
            grid.SetRowLabelValue(row, str(row))
            grid.AutoSizeRowLabelSize(row)
        for col, col_name in enumerate(columns):
            grid.SetColLabelValue(col, _(col_name) + u'↓')
            grid.AutoSizeColLabelSize(col)
            if col_name == 'count':
                cell_attr = wx.grid.GridCellAttr()
                cell_attr.SetAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
                grid.SetColAttr(col, cell_attr)
            self.param['column_sort'].append('+')
        for row, author in enumerate(authors):
            for col, col_name in enumerate(columns):
                value = getattr(author, col_name)
                if not isinstance(value, (string_type, unicode_type)):
                    value = str(value)
                grid.SetCellValue(row, col, value)
        grid.AutoSizeColumns()
        grid.AutoSizeRows()
        grid.Bind(wx.grid.EVT_GRID_COL_SORT, self.OnSort)

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

    def OnSort(self, event):
        authors = self.param['authors']
        columns = self.param['columns']
        column_sort = self.param['column_sort']
        sort_col = event.GetCol()
        column_name = columns[sort_col]
        sort_dir = column_sort[sort_col]
        if sort_dir == '+':
            reverse = True
            sort_dir = '-'
            sort_sign = u'↑'
        elif sort_dir == '-':
            reverse = False
            sort_dir = '+'
            sort_sign = u'↓'
        else:
            raise ValueError('Unknown sort direction "%s"' % sort_dir)
        authors.sort(
            key=lambda a, column_name=column_name: getattr(a, column_name),
            reverse=reverse)
        column_sort[sort_col] = sort_dir
        _ = getattr(translations, 'ugettext', None) or translations.gettext
        grid = self.grid
        for col, col_name in enumerate(columns):
            grid.SetColLabelValue(col, _(col_name) + u'↓')
        grid.SetColLabelValue(sort_col, _(column_name) + sort_sign)
        for row, author in enumerate(authors):
            for col, col_name in enumerate(columns):
                value = getattr(author, col_name)
                if not isinstance(value, (string_type, unicode_type)):
                    value = str(value)
                grid.SetCellValue(row, col, value)


class ListAuthorsWindow(GridWindow):

    session_config_section_name = 'list_authors'
    window_title = u"m_Librarian: Список авторов"
    GridPanelClass = ListAuthorsPanel
