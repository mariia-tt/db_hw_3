import MySQLdb
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import * 
from PyQt6 import uic
import sys
import numpy as np
import os

class AddWindow(QDialog):
    def __init__(self, activeTable, db, header_labels):
        super(AddWindow, self).__init__()
        uic.loadUi("./ui/add.ui", self)  
        self.activeTable = activeTable
        self.db = db
        self.header_labels = header_labels   
        self.setWindowTitle("Add data")

        self.pbAdd.setText("Add")
        self.pbClose.setText("Close")
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
        
        self.pbAdd.clicked.connect(self.add)

    def add(self):
        try:
            query = "INSERT INTO {} VALUES (".format(self.activeTable)
            for i in range(0, len(self.lineEdits), 1):
              element = self.lineEdits[i].text()
              if element != '':
                try:
                  element = int(element)
                except:
                  element = "'{}'".format(element)
                query += "{},".format(element)
              else:
                break
            query = query[:-1]
            query += ");"
            cursor = self.db.cursor()
            cursor.execute(query)
            cursor.close()
            self.db.commit()
            print(query)
            self.close()
        except Exception as e:
            print(e)
