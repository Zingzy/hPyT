from hPyT import *

# ---------- wxPython ----------

import wx

app = wx.App()

window = wx.Frame(parent=None, title='hTkT')

title_bar.hide(window) 
# title_bar.unhide(window)

maximize_button.disable(window) # disables maximize button
# maximize_button.enable(window)

minimize_button.disable(window) # disables minimize button
# minimize_button.enable(window)

window_flash.flash(window, 10) # flashes the window 10 times
# window_flash.stop(window) # stops flashing immediately

opacity.set(window, 0.5) # sets the opacity of the window to 50%

window.Show()
app.MainLoop()