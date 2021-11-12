import sys
from PyQt5.QtWidgets import QApplication

from main_window import *
from json_controller import load_points
import globals as gb


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gb.form = MainWindow()

    load_points()

    gb.form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
