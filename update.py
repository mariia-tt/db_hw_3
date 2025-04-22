import MySQLdb
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import * 
from PyQt6 import uic
import sys
import numpy as np
import os

class UpdateData(QDialog):
    def __init__(self, dataTable, activeTable, db, header_labels):
        super(UpdateData, self).__init__()
        uic.loadUi("./ui/add.ui", self)  

        self.activeTable = activeTable
        self.db = db
        self.dataTable = dataTable
        self.header_labels = header_labels   
        self.setWindowTitle("Update Data")
        self.curRow = self.dataTable.currentRow()
        self.ColNum = self.dataTable.columnCount()

        self.pbAdd.setText("Update")
        self.pbClose.setText("Close")
        self.pbClose.clicked.connect(self.close)

        self.pbAdd.clicked.connect(self.UpdateData)
        self.pbClose.clicked.connect(self.close)
        
        self.labels = sorted(self.findChildren(QLabel), key=lambda x: int(''.join(filter(str.isdigit, x.objectName()))))
        self.lineEdits = sorted(self.findChildren(QLineEdit), key=lambda x: int(''.join(filter(str.isdigit, x.objectName()))))
        for obj in range(0, len(self.labels), 1):
            self.labels[obj].setVisible(False)
            self.lineEdits[obj].setVisible(False)

        for obj in range(0, len(self.header_labels), 1):
            self.labels[obj].setVisible(True)
            self.labels[obj].setText(header_labels[obj])
            self.lineEdits[obj].setVisible(True)
            self.lineEdits[obj].setText(self.dataTable.item(self.curRow, obj).text())

    def UpdateData(self):
      try:
        query =  "UPDATE {} SET ".format(self.activeTable)
        for i in range(0, self.ColNum, 1):
          element = self.lineEdits[i].text()

          if element != '':
            try:
              element = int(element)
            except:
              element = "'{}'".format(element)
            query += "{} = {}, ".format(self.header_labels[i], element)
          
        query = query[:-2]
        query += " WHERE {} = '{}'".format(self.header_labels[0], self.lineEdits[0].text())
        print(query)
        cursor = self.db.cursor()
        cursor.execute(query)
        cursor.close()
        self.db.commit()
        self.close()

      except MySQLdb.IntegrityError:
        errorMessage = QMessageBox()
        errorMessage.setText("Помилка: повторення первинного ключа")
        errorMessage.exec_()
      except MySQLdb.OperationalError as error:
        print(error)
        errorMessage = QMessageBox()
        errorMessage.setText("Помилка: введено неправильні дані")
        errorMessage.exec()
