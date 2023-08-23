from hPyT import *

# ---------- PyQT5 ----------

import sys
from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()

title_bar.hide(window) # hides title bar
# title_bar.unhide(window)

window.show()
sys.exit(app.exec_())