import MySQLdb
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import uic
import sys
import numpy as np
import os
from add import *
from update import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("./ui/main.ui", self)     
        self.setWindowTitle("Music Compositions")

        self.errorMessage = QMessageBox()
        self.show()
        self.db = MySQLdb.connect(
            host="127.0.0.1",
            port=3306,
            user= "root",
            passwd= "Qwerty7890@",
            db="music_DB"
        )

        self.cur = self.db.cursor()
        self.cur.execute("SHOW TABLES;")
        self.tables = self.cur.fetchall()
        self.tables = np.array(self.tables)
        directory = "./sql/"
        self.listQuery = [os.path.splitext(file)[0] for file in os.listdir(directory)]
        
        for btn in self.findChildren(QPushButton):
            if btn.objectName() in self.tables:
                btn.clicked.connect(self.selectTable)
            elif btn.objectName() in self.listQuery:
                btn.clicked.connect(self.currentQuery)

        self.Album.click()
        self.pb_delete.clicked.connect(self.delete_data)
        self.pb_add.clicked.connect(self.add_data)
        self.pb_edit.clicked.connect(self.update_data)

    def selectTable(self):
        self.activeTable = self.sender().objectName()
        self.query = f"SELECT * FROM `{self.activeTable}`"
        self.execute_query()

    def currentQuery(self):
        queryName = self.sender().objectName()
        path = f"./sql/{queryName}.sql"
        self.query = open(path, "r").read()
        self.execute_query()

    def delete_data(self):
        try:
            query = f"DELETE FROM `{self.activeTable}` WHERE "
            curRow = self.dataTable.currentRow()
            lenght = len(self.primary_keys)
            for i in range(0, lenght, 1):
                item = self.dataTable.item(curRow, i).text()
                if lenght > 1 and i != lenght - 1:
                    query += f"{self.primary_keys[i]} = '{item}' AND "
                else:
                    query +=f"{self.primary_keys[i]} = '{item}'"
            try:
                print(query)
                cursor = self.db.cursor()
                cursor.execute(query)
                cursor.close() 
                self.db.commit()
                self.refresh_table()
            except Exception as e:
                self.errorMessage.setText(f"error {e}")
                self.errorMessage.exec_()
        except Exception as e:
            self.errorMessage.setText(f"error {e}")
            self.errorMessage.exec_()

    def add_data(self):
        self.add_window = AddWindow(self.activeTable, self.db, self.header_labels)
        self.add_window.setModal(True)
        self.add_window.exec()
        self.refresh_table()

    def update_data(self):
        self.add_window = UpdateData(self.dataTable, self.activeTable, self.db, self.header_labels)
        self.add_window.setModal(True)
        self.add_window.exec()
        self.refresh_table()

    def click_button_by_name(self, button_name):
        button = self.findChild(QPushButton, button_name)
        if button:
            button.click()

    def execute_query(self):
        try:
            cursor = self.db.cursor()
            query = f"SHOW INDEX FROM `{self.activeTable}` WHERE Key_name = 'PRIMARY'"
            cursor.execute(query)
            self.primary_keys = [row[4] for row in cursor.fetchall()]
            cursor.close()
            cursor = self.db.cursor()
            sql_query = self.query
            cursor.execute(sql_query)
            results = cursor.fetchall()
            self.dataTable.setRowCount(len(results))
            self.dataTable.verticalHeader().setVisible(False)
            self.dataTable.setColumnCount(len(cursor.description))
            self.header_labels = [desc[0] for desc in cursor.description]
            self.dataTable.setHorizontalHeaderLabels(self.header_labels)
            self.header = self.dataTable.horizontalHeader()      
            for row_num, row_data in enumerate(results):
                for col_num, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.dataTable.setItem(row_num, col_num, item)
                    self.header.setSectionResizeMode(col_num, QHeaderView.ResizeMode.Stretch)
            cursor.close()
        except MySQLdb.Error as e:
            print(f"MySQL Error: {e}")

    def refresh_table(self):
        if hasattr(self, 'activeTable'):
            self.query = f"SELECT * FROM `{self.activeTable}`"
            self.execute_query()

def main():
    app = QApplication([])
    window = MainWindow()
    app.exec()

if __name__ == '__main__':
    main()
