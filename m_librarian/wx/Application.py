# coding: utf-8

import wx, wx.adv
from ..__version__ import __version__


class MainWindow(wx.Frame):

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
        aboutInfo.SetWebSite(u'https://phdru.name/Software/Python/m_librarian/')
        aboutInfo.SetCopyright(u'(C) 2023 Олег Бройтман')
        aboutInfo.SetLicense(u'GPL')
        wx.adv.AboutBox(aboutInfo)


class Application(wx.App):

    def OnInit(self):
        frame = MainWindow(None, -1, u"m_Librarian")
        frame.InitMenu()
        frame.Show(True)
        self.SetTopWindow(frame)
        return True
