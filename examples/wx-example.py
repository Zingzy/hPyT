from hPyT import *

# ---------- wxPython ----------

import wx

app = wx.App()

window = get_wxPython()()

window.hide_maximize_minimize_button()

window.Show()
app.MainLoop()