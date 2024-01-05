# coding: utf-8

import wx, wx.grid  # noqa: E401 multiple imports on one line
from ..compat import string_type, unicode_type
from ..translations import translations
from .AWindow import AWindow


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
        list_authors_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(list_authors_sizer)

        grid = wx.grid.Grid(self)
        list_authors_sizer.Add(grid, 0, wx.EXPAND, 0)

        self.InitGrid(grid, search_authors_results)

    def InitGrid(self, grid, search_authors_results):
        _ = getattr(translations, 'ugettext', None) or translations.gettext
        authors = search_authors_results['authors']
        columns = search_authors_results['columns']
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
