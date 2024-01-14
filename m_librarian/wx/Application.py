import wx
from .AWindow import AWindow
from .SearchPanels import SearchAuthorsPanel, SearchBooksPanel


class MainWindow(AWindow):

    session_config_section_name = 'main_window'
    window_title = u"m_Librarian"

    def OnInit(self):
        AWindow.OnInit(self)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vsizer)

        search_authors_panel = SearchAuthorsPanel(self)
        search_books_panel = SearchBooksPanel(self)
        vsizer.Add(search_authors_panel, 0, wx.EXPAND, 0)
        vsizer.Add(search_books_panel, 0, wx.EXPAND, 0)


class Application(wx.App):

    def OnInit(self):
        frame = MainWindow()
        self.SetTopWindow(frame)
        return True
