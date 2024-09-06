import sys
import os
try:
    from PyQt6.QtWidgets import QApplication, QProgressBar, QVBoxLayout, QWidget, QPushButton
    from PyQt6.QtCore import Qt, QTimer
except ImportError:
    os.system("pip install PyQt6")
    from PyQt6.QtWidgets import QApplication, QProgressBar, QVBoxLayout, QWidget, QPushButton
    from PyQt6.QtCore import Qt, QTimer
try:
    import qdarktheme
except ImportError:
    os.system("pip install pyqtdarktheme==2.1.0 --ignore-requires-python")
    import qdarktheme
from hPyT import rainbow_title_bar

class RainbowProgressBar(QProgressBar):
    def __init__(self, *args, interval=int, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_color)
        self.timer.start(interval)

    def update_color(self):
        # get current title bar color from the rainbow_title_bar
        r,g,b = rainbow_title_bar.get_current_color()
        
        # set the current title bar color as the current progressbar color
        self.setStyleSheet(f"QProgressBar::chunk {{ background-color: rgb({r}, {g}, {b}); }}")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # initialize the window
        self.setWindowTitle('"Rainbow ProgressBar" hPyT Sync Example')
        self.setGeometry(100, 100, 600, 400)
        qdarktheme.setup_theme(theme="dark", custom_colors={"[dark]": {"primary": "#FFFFFF"}})

        self.interval = 30 # define the interval for color updates
        window = self.window() # define the window for the rainbow title bar
        
        # Start the rainbow title bar effect for the winow
        rainbow_title_bar.start(window, interval=self.interval)

        # initialize the layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # initialize the custom color changing progress bar class
        self.progress_bar = RainbowProgressBar(self, interval=self.interval) # in order to synchronize the colors make sure the rainbow title bar and your custom color changing widget (here: a progressbar) use the same interval for color updates
        self.progress_bar.setGeometry(50, 50, 500, 50)
        self.progress_bar.setRange(0, 100)
        
        # create a button which starts a progress simulation for the progressbar
        self.start_button = QPushButton("start")
        self.start_button.clicked.connect(self.start_progress_simulation)
        
        # define the layout
        layout.addStretch()
        layout.addWidget(self.progress_bar, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout.addStretch()
        
        # initialize a timer for the progressbar-progress simulation
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.progress_simulation)
        
    def start_progress_simulation(self):
        self.pb_value = 0
        progress_update_interval = 500
        
        self.progress_timer.start(progress_update_interval)
        
    def progress_simulation(self):
        self.pb_value += 5
        self.progress_bar.setValue(self.pb_value)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
