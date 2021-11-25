import sys
from PyQt5 import uic
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit

names = ['ID', 'title', 'degree', 'type', 'description', 'price', 'volume']


def view(other):
    other.table.clear()
    other.table.setRowCount(0)
    con = sqlite3.connect('coffee.sqlite')
    cur = con.cursor()
    result = list(cur.execute(f"""SELECT * FROM info""").fetchall())
    con.close()
    other.table.setColumnCount(7)
    for i in range(7):
        other.table.setHorizontalHeaderItem(i, QTableWidgetItem(names[i]))
    for i, row in enumerate(result):
        other.table.setRowCount(other.table.rowCount() + 1)
        for j, elem in enumerate(row):
            item = QTableWidgetItem(str(elem))
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            other.table.setItem(i, j, item)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        view(self)
        self.add.clicked.connect(self.click)
        self.pushButton_2.clicked.connect(self.click)

    def click(self):
        if self.sender().text() == 'добавить':
            self.second_form = Dialog(self, self.sender().text())
        else:
            if not self.table.item(self.table.currentRow(), 0) is None:
                a = self.table.item(self.table.currentRow(), 0).text()
                b = []
                for elem in [1, 2, 4, 5, 6, 3]:
                    b.append(self.table.item(self.table.currentRow(), elem).text())
                self.second_form = Dialog(self, self.sender().text(), args=b, id=a)
        self.second_form.show()

    def view(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        result = list(cur.execute(f"""SELECT * FROM info""").fetchall())
        con.close()
        self.table.setColumnCount(7)
        for i in range(7):
            self.table.setHorizontalHeaderItem(i, QTableWidgetItem(self.names[i]))
        for i, row in enumerate(result):
            self.table.setRowCount(self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                item = QTableWidgetItem(str(elem))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(i, j, item)


class Dialog(QMainWindow):
    def __init__(self, other, send, args=None, id=None):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.label.hide()
        self.other, self.send, self.id = other, send, id
        self.label.resize(300, 20)
        self.pushButton.clicked.connect(self.click)
        if self.send == 'изменить':
            self.pushButton.setText('изменить запись')
            elems = [self.lineEdit_2, self.lineEdit_3, self.lineEdit_4, self.lineEdit_5, self.lineEdit_6]
            for i in range(len(elems)):
                elems[i].setText(args[i])
            self.comboBox.setCurrentIndex(int(args[-1]) - 1)



    def click(self):
        b, c, = self.lineEdit_2.text(), self.lineEdit_3.text()
        d, e, f = self.comboBox.currentText(), self.lineEdit_4.text(), self.lineEdit_5.text()
        g = self.lineEdit_6.text()
        if b and c and d and e and f and g:
            if not f.isdigit():
                self.label.show()
                self.label.move(40, 215)
                self.label.setText('цена может быть только целым числом')
                return None
            if not g.isdigit():
                self.label.show()
                self.label.move(40, 215)
                self.label.setText('объём может быть только целым числом')
                return None
            else:
                d = 1 if d == 'молотый' else 2
                con = sqlite3.connect('coffee.sqlite')
                cur = con.cursor()
                if self.send == 'добавить':
                    a = 'INSERT INTO info(title, degree, type, description, price, volume)'
                    cur.execute(f"""{a} VALUES("{b}", "{c}", {d}, "{e}", {f}, {g})""")
                else:
                    cur.execute(f"""
UPDATE info
SET title = "{b}"
WHERE id = {self.id}
""")
                    cur.execute(f"""
UPDATE info
SET degree = "{c}"
WHERE id = {self.id}
""")
                    cur.execute(f"""
UPDATE info
SET type = {d}
WHERE id = {self.id}
""")
                    cur.execute(f"""
UPDATE info
SET description = "{e}"
WHERE id = {self.id}
""")
                    cur.execute(f"""
UPDATE info
SET price = {f}
WHERE id = {self.id}
""")
                    cur.execute(f"""
UPDATE info
SET volume = {g}
WHERE id = {self.id}
""")
                con.commit()
                con.close()
                view(self.other)
                self.close()
        else:
            self.label.show()
            self.label.move(90, 215)
            self.label.setText('заполните все поля')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
