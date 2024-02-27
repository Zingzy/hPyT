from hPyT import *

# ---------- Tkinter ----------

from customtkinter import *

window = CTk()
window.title("hPyT")
window.geometry("400x100")

maximize_minimize_button.hide(window) # hides both maximize and minimize button
# maximize_minimize_button.unhide(window)

all_stuffs.hide(window) # hides close button
# all_stuffs.unhide(window)

title_bar.hide(window) # hides title bar
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

# check out the readme.md file for other functions

window.mainloop()