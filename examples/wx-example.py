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

rainbow_title_bar.start(window) # starts the rainbow effect on taskbar
# rainbow_title_bar.stop(window) # stops the rainbow effect on taskbar

rainbow_border.start(window) # starts the rainbow effect on border
# rainbow_border.stop(window) # stops the rainbow effect on border

# check out the readme.md file for other functions

window.Show()
app.MainLoop()