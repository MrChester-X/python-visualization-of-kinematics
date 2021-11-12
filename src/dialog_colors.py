from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, \
    QColorDialog, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import sqlite3

import globals as gb


class ColorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Настройка цветов")
        self.resize(350, 650)

        self.table = QTableWidget(self)
        self.table.resize(250, 500)
        self.table.move(50, 50)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "Цвет"])
        self.table.cellDoubleClicked.connect(self.hook_click)

        self.button_add = QPushButton(self)
        self.button_add.move(50, 560)
        self.button_add.resize(250, 23)
        self.button_add.setText("Добавить новый цвет")
        self.button_add.clicked.connect(self.hook_add)

        self.button_delete = QPushButton(self)
        self.button_delete.move(50, 590)
        self.button_delete.resize(250, 23)
        self.button_delete.setText("Удалить выбранные цвета")
        self.button_delete.clicked.connect(self.hook_delete)

        self.con = sqlite3.connect(gb.path_sqlite_colors)

        self.load_table()

    def load_table(self):
        gb.pen_colors.clear()

        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM Colors").fetchall()

        for i in result:
            gb.pen_colors.append([int(i[0]),
                                 [int(x) for x in i[1].split(", ")]])

        self.fill_table()

    def fill_table(self):
        self.table.setRowCount(len(gb.pen_colors))

        for i, color in enumerate(gb.pen_colors):
            item1 = QTableWidgetItem(str(color[0]))
            item1.setFlags(Qt.ItemFlag(int(item1.flags()) &
                                       ~Qt.ItemIsEditable))
            item2 = QTableWidgetItem()
            item2.setFlags(Qt.ItemFlag(int(item2.flags()) &
                                       ~Qt.ItemIsEditable))
            item2.setBackground(QColor(*color[1]))

            self.table.setItem(i, 0, item1)
            self.table.setItem(i, 1, item2)

    def hook_click(self, row, column):
        if column != 1:
            return

        color = QColorDialog.getColor()
        if color.isValid():
            gb.pen_colors[row][1] = [color.red(), color.green(), color.blue()]

            cur = self.con.cursor()
            que = f"UPDATE Colors SET Color = " \
                  f"'{', '.join([str(i) for i in gb.pen_colors[row][1]])}' " \
                  f"WHERE ID = {int(gb.pen_colors[row][0])}"
            cur.execute(que)
            self.con.commit()

        self.load_table()

    def hook_add(self):
        cur = self.con.cursor()
        que = f"INSERT INTO Colors(Color) VALUES " \
              f"('{', '.join([str(i) for i in gb.default_color])}')"
        cur.execute(que)
        self.con.commit()

        self.load_table()

    def hook_delete(self):
        if not len(gb.pen_colors):
            return

        rows = list(set([i.row() for i in self.table.selectedItems()]))
        ids = [int(gb.pen_colors[i][0]) for i in rows]

        cur = self.con.cursor()
        cur.execute("DELETE FROM Colors WHERE ID IN (" + ", ".join(
            '?' * len(ids)) + ")", ids)
        self.con.commit()

        self.load_table()
