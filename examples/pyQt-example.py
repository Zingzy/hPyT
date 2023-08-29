from hPyT import *

# ---------- PyQT5 ----------
from PyQt5 import QtWidgets
import sys


app = QtWidgets.QApplication(sys.argv)
window = get_PyQt5()()

window.hide_maximize_minimize_button()

window.show()
sys.exit(app.exec_())