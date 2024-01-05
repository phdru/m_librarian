import wx
from .AWindow import AWindow
from .SearchPanel import SearchPanel


class MainWindow(AWindow):

    session_config_section_name = 'main_window'
    window_title = u"m_Librarian"

    def OnInit(self):
        AWindow.OnInit(self)
        SearchPanel(self)


class Application(wx.App):

    def OnInit(self):
        frame = MainWindow()
        self.SetTopWindow(frame)
        return True
