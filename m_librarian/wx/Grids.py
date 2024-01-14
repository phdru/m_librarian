import wx, wx.grid  # noqa: E401 multiple imports on one line
from .AWindow import AWindow


class GridPanel(wx.Panel):

    def __init__(self, parent, param):
        wx.Panel.__init__(self, parent)
        self.param = param

        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vsizer)

        self.grid = grid = wx.grid.Grid(self)
        vsizer.Add(grid, 0, wx.EXPAND, 0)

        grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.OnDClick)
        grid.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        self.InitGrid()
        grid.SetFocus()

        parent.Bind(wx.EVT_ACTIVATE, self.OnActivate)
        parent.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(wx.EVT_ACTIVATE, self.OnActivate)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)

    def InitGrid(self):
        raise NotImplementedError

    def OnDClick(self, event):
        raise NotImplementedError

    def OnKeyDown(self, event):
        raise NotImplementedError

    def OnActivate(self, event):
        if event.GetActive():
            self.grid.SetFocus()

    def OnSetFocus(self, event):
        self.grid.SetFocus()


class GridWindow(AWindow):

    # Subclasses must override these
    session_config_section_name = None
    window_title = None
    GridPanelClass = GridPanel

    def __init__(self, parent, param):
        self.param = param
        AWindow.__init__(self, parent)

    def OnInit(self):
        AWindow.OnInit(self)
        self.panel = self.GridPanelClass(self, self.param)
