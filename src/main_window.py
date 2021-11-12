import sys
from string import Template
from PyQt5.QtWidgets import QWidget, QMainWindow, \
    QPushButton, QLabel, QColorDialog, QMessageBox, QAction, QListWidget, \
    QGroupBox, QLineEdit, QRadioButton, QMenuBar, QMenu, QStatusBar
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import Qt, QRect
import pyqtgraph as pg

from functions import *
import globals as gb
from point_controller import Point
from dialog_colors import ColorWindow
from json_controller import load_points, save_points


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.make_build()
        self.clear_all()
        self.create_list()
        self.hook_signals()

    def initUI(self):
        self.resize(880, 940)
        self.move(300, 25)
        self.setWindowTitle("Visualization of kinematics")

        self.action_2 = QAction(self)
        self.action_2.setText("123")

        self.action_save = QAction(self)
        self.action_save.setText("Сохранить")

        self.action_load = QAction(self)
        self.action_load.setText("Загрузить")

        self.action_colors = QAction(self)
        self.action_colors.setText("Цвета")

        self.centralwidget = QWidget(self)

        self.button_build = QPushButton(self.centralwidget)
        self.button_build.setGeometry(QRect(500, 250, 311, 51))
        self.button_build.setText("Построить графики")

        self.points_list = QListWidget(self.centralwidget)
        self.points_list.setGeometry(QRect(40, 20, 301, 221))

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QRect(40, 360, 801, 521))
        self.groupBox.setTitle("Графики")

        self.graphic1 = pg.PlotWidget(self.groupBox)
        self.graphic1.setGeometry(QRect(440, 30, 331, 231))

        self.graphic2 = pg.PlotWidget(self.groupBox)
        self.graphic2.setGeometry(QRect(30, 30, 331, 231))

        self.graphic3 = pg.PlotWidget(self.groupBox)
        self.graphic3.setGeometry(QRect(30, 280, 331, 231))

        self.graphic4 = pg.PlotWidget(self.groupBox)
        self.graphic4.setGeometry(QRect(440, 280, 331, 231))

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QRect(370, 20, 451, 221))
        self.groupBox_2.setTitle("Настройки точки")

        self.input_name = QLineEdit(self.groupBox_2)
        self.input_name.setGeometry(QRect(240, 20, 113, 20))

        self.input_y = QLineEdit(self.groupBox_2)
        self.input_y.setGeometry(QRect(240, 50, 113, 20))

        self.input_x = QLineEdit(self.groupBox_2)
        self.input_x.setGeometry(QRect(240, 80, 113, 20))

        self.input_speed = QLineEdit(self.groupBox_2)
        self.input_speed.setGeometry(QRect(240, 110, 113, 20))

        self.input_alpha = QLineEdit(self.groupBox_2)
        self.input_alpha.setGeometry(QRect(240, 140, 113, 20))

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setGeometry(QRect(80, 80, 151, 20))
        self.label_3.setText("Начальная координата x (м)")

        self.label = QLabel(self.groupBox_2)
        self.label.setGeometry(QRect(100, 110, 131, 20))
        self.label.setText("Начальная скорость (м/с)")

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setGeometry(QRect(140, 20, 91, 20))
        self.label_6.setText("Название точки")

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setGeometry(QRect(120, 140, 111, 20))
        self.label_2.setText("Угол к горизонту (°)")

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setGeometry(QRect(80, 50, 151, 20))
        self.label_4.setText("Начальная координата y (м)")

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setGeometry(QRect(160, 170, 71, 20))
        self.label_5.setText("Выбор цвета")

        self.button_color = QPushButton(self.groupBox_2)
        self.button_color.setGeometry(QRect(240, 172, 111, 21))

        self.button_add = QPushButton(self.centralwidget)
        self.button_add.setGeometry(QRect(40, 250, 301, 23))
        self.button_add.setText("Добавить точку")

        self.button_del_current = QPushButton(self.centralwidget)
        self.button_del_current.setGeometry(QRect(40, 280, 141, 23))
        self.button_del_current.setText("Удалить текущее")

        self.button_del_select = QPushButton(self.centralwidget)
        self.button_del_select.setGeometry(QRect(200, 280, 141, 23))
        self.button_del_select.setText("Удалить выбранное")

        self.button_select_all = QPushButton(self.centralwidget)
        self.button_select_all.setGeometry(QRect(40, 310, 141, 23))
        self.button_select_all.setText("Выбрать все")

        self.button_unselect_all = QPushButton(self.centralwidget)
        self.button_unselect_all.setGeometry(QRect(200, 310, 141, 23))
        self.button_unselect_all.setText("Очистить выбор")

        self.radiobutton_all = QRadioButton(self.centralwidget)
        self.radiobutton_all.setGeometry(QRect(510, 310, 82, 17))
        self.radiobutton_all.setText("Все точки")
        self.radiobutton_all.setChecked(True)

        self.radiobutton_selected = QRadioButton(self.centralwidget)
        self.radiobutton_selected.setGeometry(QRect(510, 330, 151, 17))
        self.radiobutton_selected.setText("Только выбранные точки")

        self.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 879, 21))

        self.menu = QMenu(self.menubar)
        self.menu.setTitle("Настройки")

        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setTitle("Файл")

        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.action_colors)
        self.menu_2.addAction(self.action_save)
        self.menu_2.addAction(self.action_load)

        self.input_y.setValidator(QDoubleValidator())
        self.input_x.setValidator(QDoubleValidator())
        self.input_speed.setValidator(QDoubleValidator())
        self.input_alpha.setValidator(QDoubleValidator())

        self.toggle_all_inputs(False)
        self.styles = {"color": "red", "font-size": "20px"}

    def make_build(self):
        self.build_graph_x()
        self.build_graph_y()
        self.build_graph_xy()
        self.build_graph_s()

    def clear_all(self):
        self.graphic1.clear()
        self.graphic2.clear()
        self.graphic3.clear()
        self.graphic4.clear()

    def create_list(self):
        # self.add_point(*gb.default_point)
        # self.set_current_point(0)
        pass

    def hook_signals(self):
        self.button_build.clicked.connect(self.make_build)
        self.button_add.clicked.connect(self.hook_add_point)
        self.button_del_current.clicked.connect(self.hook_delete_current)
        self.button_del_select.clicked.connect(self.hook_delete_select)
        self.button_select_all.clicked.connect(self.hook_select_all)
        self.button_unselect_all.clicked.connect(self.hook_unselect_all)
        self.button_color.clicked.connect(self.hook_color)
        self.points_list.itemPressed.connect(self.item_click)
        self.input_name.textChanged.connect(self.edit_input_name)
        self.input_y.editingFinished.connect(self.edit_input_y)
        self.input_x.editingFinished.connect(self.edit_input_x)
        self.input_speed.editingFinished.connect(self.edit_input_speed)
        self.input_alpha.editingFinished.connect(self.edit_input_alpha)
        self.action_colors.triggered.connect(self.hook_colors)
        self.action_save.triggered.connect(self.hook_save)
        self.action_load.triggered.connect(self.hook_load)

    def build_graph_x(self):
        self.graphic1.clear()
        self.graphic1.setBackground("w")
        self.graphic1.showGrid(x=True, y=True)

        self.graphic1.setLabel("left", "Координата, x", **self.styles)
        self.graphic1.setLabel("bottom", "Время, t", **self.styles)

        for point in gb.points:
            if self.is_build_selected() and \
                    point.get_item().checkState() != Qt.Checked:
                continue

            array = get_array_x(point.get_x(), point.get_speed(),
                                point.get_alpha(), point.get_time())
            self.graphic1.plot(*array, pen=self.get_pen(point.get_color()))

    def build_graph_y(self):
        self.graphic2.clear()
        self.graphic2.setBackground("w")
        self.graphic2.showGrid(x=True, y=True)

        self.graphic2.setLabel("left", "Координата, y", **self.styles)
        self.graphic2.setLabel("bottom", "Время, t", **self.styles)

        for point in gb.points:
            if self.is_build_selected() and \
                    point.get_item().checkState() != Qt.Checked:
                continue

            array = get_array_y(point.get_y(), point.get_speed(),
                                point.get_alpha(), point.get_time())
            self.graphic2.plot(*array, pen=self.get_pen(point.get_color()))

    def build_graph_xy(self):
        self.graphic3.clear()
        self.graphic3.setBackground("w")
        self.graphic3.showGrid(x=True, y=True)

        self.graphic3.setLabel("left", "Координата, y", **self.styles)
        self.graphic3.setLabel("bottom", "Координата, x", **self.styles)

        for point in gb.points:
            if self.is_build_selected() and \
                    point.get_item().checkState() != Qt.Checked:
                continue

            array = [get_array_x(point.get_x(), point.get_speed(),
                                 point.get_alpha(), point.get_time())[1],
                     get_array_y(point.get_y(), point.get_speed(),
                                 point.get_alpha(), point.get_time())[1]]
            self.graphic3.plot(*array, pen=self.get_pen(point.get_color()))

    def build_graph_s(self):
        self.graphic4.clear()
        self.graphic4.setBackground("w")
        self.graphic4.showGrid(x=True, y=True)

        self.graphic4.setLabel("left", "Путь, S", **self.styles)
        self.graphic4.setLabel("bottom", "Время, t", **self.styles)

        for point in gb.points:
            if self.is_build_selected() and \
                    point.get_item().checkState() != Qt.Checked:
                continue

            array = get_array_s(point.get_x(), point.get_y(),
                                point.get_speed(), point.get_alpha(),
                                point.get_time())
            self.graphic4.plot(*array, pen=self.get_pen(point.get_color()))

    def item_click(self, item):
        self.current_point = [i.get_item() for i in gb.points].index(item)
        point = gb.points[self.current_point]

        self.set_name(point.get_name())
        self.set_y(point.get_y())
        self.set_x(point.get_x())
        self.set_speed(point.get_speed())
        self.set_alpha(point.get_alpha())
        self.set_color(point.get_color())

    def hook_add_point(self):
        self.add_point(*gb.default_point)

    def hook_delete_select(self):
        array = [(i, point) for i, point in enumerate(gb.points)
                 if point.get_item().checkState() == Qt.Checked]
        if not len(array):
            return

        valid = QMessageBox.question(
            self, "Подтверждение удаления",
            f"Вы точно хотите удалить точки ({len(array)}): "
            f"{', '.join([i[1].get_name() for i in array])}?",
            QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            for i, point in reversed(array):
                self.delete_point(i)

    def hook_delete_current(self):
        if not len(gb.points):
            return

        valid = QMessageBox.question(
            self, "Подтверждение удаления",
            f"Вы точно хотите удалить точку "
            f"{self.get_current_point().get_name()}?",
            QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            self.delete_point(self.current_point)

    def hook_select_all(self):
        for point in gb.points:
            point.get_item().setCheckState(Qt.Checked)

    def hook_unselect_all(self):
        for point in gb.points:
            point.get_item().setCheckState(Qt.Unchecked)

    def hook_color(self):
        if not self.inputs_enabled:
            return

        color = QColorDialog.getColor()
        if color.isValid():
            self.set_color([color.red(), color.green(), color.blue()])

    def add_point(self, *args):
        gb.points.append(Point(*args))
        self.points_list.addItem(gb.points[-1].get_item())
        self.toggle_all_inputs(True)
        self.set_current_point(len(gb.points) - 1)

    def delete_point(self, index):
        self.points_list.takeItem(index)
        del gb.points[index]

        if len(gb.points):
            self.set_current_point(max(0, self.current_point - 1))
        else:
            self.toggle_all_inputs(False)

    def edit_input_name(self):
        if not self.inputs_enabled:
            return

        self.get_current_point().set_name(self.get_name())

    def edit_input_y(self):
        if not self.inputs_enabled:
            return

        self.get_current_point().set_y(self.get_y())

    def edit_input_x(self):
        if not self.inputs_enabled:
            return

        self.get_current_point().set_x(self.get_x())

    def edit_input_speed(self):
        if not self.inputs_enabled:
            return

        self.get_current_point().set_speed(self.get_speed())

    def edit_input_alpha(self):
        if not self.inputs_enabled:
            return

        self.get_current_point().set_alpha(self.get_alpha())

    def hook_colors(self):
        self.window = ColorWindow()
        self.window.show()

    def hook_save(self):
        save_points()

    def hook_load(self):
        load_points()

    def get_current_point(self):
        if len(gb.points):
            return gb.points[self.current_point]

        return None

    def get_pen(self, color):
        return pg.mkPen(width=2, color=color)

    def get_name(self):
        return self.input_name.text()

    def set_name(self, name):
        self.input_name.setText(name)

    def get_y(self):
        return float(self.input_y.text())

    def set_y(self, y):
        self.input_y.setText(str(y))

    def get_x(self):
        return float(self.input_x.text())

    def set_x(self, x):
        self.input_x.setText(str(x))

    def get_speed(self):
        return float(self.input_speed.text())

    def set_speed(self, speed):
        self.input_speed.setText(str(speed))

    def get_alpha(self):
        return float(self.input_alpha.text())

    def set_alpha(self, alpha):
        self.input_alpha.setText(str(alpha))

    def set_color(self, color):
        style = Template("QPushButton {background-color: rgb($name);}")\
            .substitute(name=", ".join([str(i) for i in color]))

        self.button_color.setStyleSheet(style)

        if self.inputs_enabled:
            self.get_current_point().set_color(color)

    def is_build_selected(self):
        if not self.inputs_enabled:
            return

        return self.radiobutton_selected.isChecked()

    def set_current_point(self, index):
        self.current_point = index
        self.points_list.setCurrentRow(index)
        self.item_click(gb.points[index].get_item())

    def toggle_all_inputs(self, value):
        self.inputs_enabled = value

        self.input_name.setReadOnly(not value)
        self.input_y.setReadOnly(not value)
        self.input_x.setReadOnly(not value)
        self.input_speed.setReadOnly(not value)
        self.input_alpha.setReadOnly(not value)

        if not value:
            self.set_name("")
            self.set_y("")
            self.set_x("")
            self.set_speed("")
            self.set_alpha("")
            self.set_color(gb.default_color)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
