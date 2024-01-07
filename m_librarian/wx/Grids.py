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

        self.InitGrid()

    def InitGrid(self):
        raise NotImplementedError


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
        self.GridPanelClass(self, self.param)
