
try:
    from m_lib.pbar.tty_pbar import ttyProgressBar
except ImportError:
    ttyProgressBar = None

if ttyProgressBar:
    class ml_ttyProgressBar(object):
        def __init__(self, width=20):
            self.max = None
            self.pbar = None
            self.width = width

        def set_max(self, max_value):
            self.max = max_value
            self.pbar = ttyProgressBar(0, max_value, width1=self.width)

        def display(self, value):
            if self.pbar:
                self.pbar.display(value)

        def close(self):
            if self.pbar:
                self.pbar.erase()
                self.pbar = None
