# coding: utf-8

import wx, wx.adv  # noqa: E401 multiple imports on one line
from ..__version__ import __version__
from .session_config import get_session_config


class AWindow(wx.Frame):

    '''
    A universal parent class for all top-level application windows

    Standard menu and ability to save/restore window size.
    '''

    # Subclasses should override these
    session_config_section_name = None
    window_title = None

    def __init__(self, parent=None):
        if self.session_config_section_name:
            session_config = get_session_config()
            width = session_config.getint(
                self.session_config_section_name, 'width', 600)
            height = session_config.getint(
                self.session_config_section_name, 'height', 400)
        else:
            width = 600
            height = 400
        wx.Frame.__init__(
            self,
            parent=parent, id=-1, title=self.window_title,
            size=wx.Size(width=width, height=height),
        )
        self.OnInit()
        self.Show(True)

    def OnInit(self):
        if self.Parent:
            self.Parent.Disable()
        self.InitMenu()
        if self.session_config_section_name:
            self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def InitMenu(self):
        MenuBar = wx.MenuBar()
        self.SetMenuBar(MenuBar)

        file_menu = wx.Menu()

        if self.Parent:
            close_win = \
                file_menu.Append(wx.ID_CLOSE, u"&Закрыть", u"Закрыть окно")
            self.Bind(wx.EVT_MENU, self.OnCloseCommand, close_win)

        quit = file_menu.Append(wx.ID_EXIT, u"&Выход", u"Выйти из программы")
        self.Bind(wx.EVT_MENU, self.OnQuit, quit)
        MenuBar.Append(file_menu, u"&Файл")

        about_menu = wx.Menu()
        about = about_menu.Append(wx.ID_ABOUT,
                                  u"&О m_Librarian", u"О m_Librarian")
        self.Bind(wx.EVT_MENU, self.OnAbout, about)
        MenuBar.Append(about_menu, u"&О программе")

    def OnCloseCommand(self, event):
        self.Close(True)

    def OnClose(self, event):
        if self.Parent:
            self.Parent.Enable()
        event.Skip()  # Call other handlers

    def OnQuit(self, event):
        wx.GetApp().ExitMainLoop()

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
        if self.session_config_section_name:
            size = event.GetSize()
            session_config = get_session_config()
            session_config.set(
                self.session_config_section_name, 'width', str(size.width))
            session_config.set(
                self.session_config_section_name, 'height', str(size.height))
            session_config.save()
        event.Skip()  # Call other handlers
