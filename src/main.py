import sys
import pyqtgraph as pg
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 1000, 700)
        self.setWindowTitle("Визуальная кинематика")

        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]

        self.widgets = []
        self.layouts = []
        self.graphs = []

        pen = pg.mkPen(color=(255, 0, 0), width=2)

        y = 10

        for _ in range(3):
            self.widgets.append(QWidget(self))
            self.widgets[-1].resize(300, 300)
            self.widgets[-1].move(10, y)

            self.graphs.append(pg.PlotWidget())

            self.graphs[-1].setBackground("w")
            self.graphs[-1].setTitle("")
            self.graphs[-1].showGrid(x=True, y=True)

            # self.graphs[-1].plot(hour, temperature, pen=pen)

            self.central = QWidget(self)
            self.central.resize(300, 300)

            self.layouts.append(QGridLayout(self.widgets[-1]))
            self.layouts[-1].addWidget(self.graphs[-1])

            y += 310

        styles = {"color": "red", "font-size": "20px"}

        self.graphs[0].setLabel("left", "Координата, x", **styles)
        self.graphs[0].setLabel("bottom", "Время, t", **styles)
        self.graphs[0].plot(hour, temperature, pen=pen)

        self.graphs[1].setLabel("left", "Координата, y", **styles)
        self.graphs[1].setLabel("bottom", "Время, t", **styles)
        self.graphs[1].plot(hour[::-1], temperature, pen=pen)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
