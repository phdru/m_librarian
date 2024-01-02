# coding: utf-8

import wx, wx.adv  # noqa: E401 multiple imports on one line
from ..__version__ import __version__
from .session_config import get_session_config


class MainWindow(wx.Frame):

    def __init__(self):
        session_config = get_session_config()
        width = session_config.getint('main_window', 'width', 600)
        height = session_config.getint('main_window', 'height', 400)
        super(wx.Frame, self).__init__(
            parent=None, id=-1, title=u"m_Librarian",
            size=wx.Size(width=width, height=height),
        )
        self.InitMenu()
        self.Show(True)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def InitMenu(self):
        MenuBar = wx.MenuBar()
        self.SetMenuBar(MenuBar)

        file_menu = wx.Menu()
        exit = file_menu.Append(wx.ID_EXIT, u"&Выход", u"Выйти из программы")
        self.Bind(wx.EVT_MENU, self.OnQuit, exit)
        MenuBar.Append(file_menu, u"&Файл")

        about_menu = wx.Menu()
        about = about_menu.Append(wx.ID_ABOUT,
                                  u"&О m_Librarian", u"О m_Librarian")
        self.Bind(wx.EVT_MENU, self.OnAbout, about)
        MenuBar.Append(about_menu, u"&О программе")

    def OnQuit(self, event):
        self.Close(True)

    def OnAbout(self, event):
        aboutInfo = wx.adv.AboutDialogInfo()
        aboutInfo.SetName(u'm_Librarian')
        aboutInfo.SetVersion(__version__)
        aboutInfo.SetDescription(
            u'Библиотекарь для библиотек LibRusEc/Flibusta')
        aboutInfo.AddDeveloper(u'Олег Бройтман')
        aboutInfo.SetWebSite(
            u'https://phdru.name/Software/Python/m_librarian/')
        aboutInfo.SetCopyright(u'(C) 2023, 2024 Олег Бройтман')
        aboutInfo.SetLicense(u'GPL')
        wx.adv.AboutBox(aboutInfo)

    def OnSize(self, event):
        """Save window size in the session config"""
        size = event.GetSize()
        session_config = get_session_config()
        session_config.set('main_window', 'width', str(size.width))
        session_config.set('main_window', 'height', str(size.height))
        session_config.save()
        event.Skip()  # Call other handlers


class Application(wx.App):

    def OnInit(self):
        frame = MainWindow()
        self.SetTopWindow(frame)
        return True
