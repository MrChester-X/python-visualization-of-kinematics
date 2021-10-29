import sys
from math import sin, cos, sqrt, radians as rd
import pyqtgraph as pg
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.make_build()
        self.clear_all()

    def initUI(self):
        uic.loadUi('form.ui', self)

        self.pen = pg.mkPen(color=(255, 0, 0), width=2)
        self.styles = {"color": "red", "font-size": "20px"}

        self.button_build.clicked.connect(self.make_build)

    def make_build(self):
        self.build_graph_x()
        self.build_graph_y()

    def clear_all(self):
        self.graphic1.clear()
        self.graphic2.clear()

    def build_graph_x(self):
        self.graphic1.clear()
        self.graphic1.setBackground("w")
        self.graphic1.showGrid(x=True, y=True)

        self.graphic1.setLabel("left", "Координата, x", **self.styles)
        self.graphic1.setLabel("bottom", "Время, t", **self.styles)

        array = get_array_x(self.get_x_start(), self.get_speed(), self.get_alpha(),
                            self.get_time())
        self.graphic1.plot(*array, pen=self.pen)

    def build_graph_y(self):
        self.graphic2.clear()
        self.graphic2.setBackground("w")
        self.graphic2.showGrid(x=True, y=True)

        self.graphic2.setLabel("left", "Координата, y", **self.styles)
        self.graphic2.setLabel("bottom", "Время, t", **self.styles)

        array = get_array_y(self.get_y_start(), self.get_speed(), self.get_alpha(), self.get_g())
        self.graphic2.plot(*array, pen=self.pen)

    def get_y_start(self):
        return float(self.input_y.text())

    def get_x_start(self):
        return float(self.input_x.text())

    def get_speed(self):
        return float(self.input_speed.text())

    def get_alpha(self):
        return float(self.input_alpha.text())

    def get_g(self):
        return float(self.input_g.text())

    def get_time(self):
        return get_flight_time(self.get_y_start(), self.get_speed(), self.get_alpha(), self.get_g())


def get_array_y(y_start, speed, alpha, g):
    array = [[], []]

    t = 0.0
    while True:
        y = y_start + (sin(rd(alpha)) * speed * t) - ((g * t ** 2) / 2)
        t += 0.001

        if y < 0:
            return array

        array[0].append(t)
        array[1].append(y)


def get_array_x(x_start, speed, alpha, time):
    array = [[], []]

    t = 0.0
    while True:
        x = x_start + (cos(rd(alpha)) * speed * t)
        t += 0.001

        if t > time:
            return array

        array[0].append(t)
        array[1].append(x)


def get_flight_time(y_start, speed, alpha, g):
    return (speed * sin(rd(alpha)) + sqrt((speed * sin(rd(alpha))) ** 2 + 2 * g * y_start)) / g


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
