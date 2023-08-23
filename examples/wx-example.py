from hPyT import *

# ---------- wxPython ----------

import wx

app = wx.App()

window = wx.Frame(parent=None, title='hTkT')

title_bar.hide(window) 
# title_bar.unhide(window)

window.Show()
app.MainLoop()