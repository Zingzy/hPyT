from hPyT import *

# ---------- PyQT5 ----------

import sys
from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()

title_bar.hide(window) # hides title bar
# title_bar.unhide(window)

maximize_button.disable(window) # disables maximize button
# maximize_button.enable(window)

minimize_button.disable(window) # disables minimize button
# minimize_button.enable(window)

window_flash.flash(window, 10) # flashes the window 10 times
# window_flash.stop(window) # stops flashing immediately

opacity.set(window, 0.5) # sets the opacity of the window to 50%


window.show()
sys.exit(app.exec_())