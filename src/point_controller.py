from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from random import choice

import globals as gb
from functions import *


class Point:
    def __init__(self, x, y, speed, alpha, name=None, color=None):
        self.x = x
        self.y = y
        self.speed = speed
        self.alpha = alpha

        if name:
            self.name = name
        else:
            self.name = f"Point #{len(gb.points) + 1}"

        self.make_item()

        if color:
            self.color = color
        else:
            self.choose_color()

    def make_item(self):
        self.item = QListWidgetItem()
        self.item.setCheckState(Qt.Unchecked)
        self.item.setText(self.name)

    def choose_color(self):
        self.set_color(choice(gb.pen_colors)[1])

    def set_color(self, color):
        self.color = color
        self.get_item().setForeground(QColor(*color))

    def get_color(self):
        return self.color

    def get_item(self):
        return self.item

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        self.get_item().setText(name)

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha

    def get_time(self):
        return get_flight_time(self.get_y(), self.get_speed(),
                               self.get_alpha())
