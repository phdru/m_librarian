# coding: utf-8

import wx


class MainWindow(wx.Frame):

    def InitMenu(self):
        MenuBar = wx.MenuBar()
        self.SetMenuBar(MenuBar)

        file_menu = wx.Menu()
        exit = file_menu.Append(wx.ID_EXIT, u"&Выход", u"Выйти из программы")
        self.Bind(wx.EVT_MENU, self.OnQuit, exit)
        MenuBar.Append(file_menu, u"&Файл")

    def OnQuit(self, event):
        self.Close(True)


class Application(wx.App):

    def OnInit(self):
        frame = MainWindow(None, -1, u"m_Librarian")
        frame.InitMenu()
        frame.Show(True)
        self.SetTopWindow(frame)
        return True
