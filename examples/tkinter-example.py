from hPyT import *

# ---------- Tkinter ----------

from customtkinter import *

window = CTk()
window.title("hTkT")
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

window.mainloop()