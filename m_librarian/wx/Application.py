import wx


class Application(wx.App):

    def OnInit(self):
        frame = wx.Frame(None, -1, u"m_Librarian")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True
