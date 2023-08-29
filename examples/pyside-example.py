from hPyT import *

# ---------- PySide2 ----------

from PySide2.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
window = get_PySide2()()

window.hide_maximize_minimize_button()

window.show()
app.exec_()