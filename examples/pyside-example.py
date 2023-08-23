from hPyT import *

# ---------- PySide2 ----------

from PySide2.QtWidgets import QApplication, QWidget
import sys

app = QApplication(sys.argv)
window = QWidget()

title_bar.hide(window) # hides title bar
# title_bar.unhide(window)

window.show()
app.exec_()