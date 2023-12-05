from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QSortFilterProxyModel
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
import pyodbc

# implementation similar to new_category.py

class NewArea(QtWidgets.QMainWindow):
    def __init__(self, ngoID):
        super().__init__()
        uic.loadUi('Screens/NGONewArea.ui' , self)

        #set window title
        self.setWindowTitle("Add New Area")

        self.model = QStandardItemModel(self.areas)
        self.proxyModel = QSortFilterProxyModel(self.areas)
        self.proxyModel.setSourceModel(self.model)
        self.areas.setModel(self.proxyModel)

        self.areas.setEditable(True)
        self.areas.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.NoInsert)
        self.areas.completer().setCompletionMode(QtWidgets.QCompleter.CompletionMode.PopupCompletion)
        self.areas.completer().setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        self.areas.lineEdit().textEdited.connect(self.proxyModel.setFilterFixedString)

        self.areaDoneBtn.clicked.connect(lambda: self.AddArea(ngoID))
        self.areaCancelBtn.clicked.connect(lambda: self.close())

        self.loadAreas(ngoID)

        self.areas.setCurrentIndex(-1)

    
    def loadAreas(self, ngoID):
        # load data into areas combo box
        connection = pyodbc.connect(
                'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
        )

        # server = 'SABIR\SQLEXPRESS'
        # database = 'NGOConnect'  # Name of your NGOConnect database 
        # connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')

        cursor = connection.cursor()

        # only get those areas which are not currently assigned to the NGO
        cursor.execute("""
            SELECT a.areaName
            FROM Area a
            WHERE a.areaCode NOT IN (
                SELECT oa.areaCode
                FROM OperatingAreas oa
                WHERE oa.ngoID = ?
            )
        """, ngoID)
        areas = cursor.fetchall()

        for area in areas:
            item = QStandardItem(area[0])
            self.model.appendRow(item)
    
    def AddArea(self, ngoID):
        areaName = self.areas.currentText()
        if areaName == "":
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Please select an area")
            Dialog.exec()
            return

        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation")
        Dialog.setText("Are you sure you want to add this area?")
        Dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Yes:
            connection = pyodbc.connect(
                'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
            )

            # server = 'SABIR\SQLEXPRESS'
            # database = 'NGOConnect'  # Name of your NGOConnect database
            # connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')
            cursor = connection.cursor()
            areaName = self.areas.currentText()

            #get areaCode
            cursor.execute("SELECT areaCode FROM Area WHERE areaName = ?", areaName)
            areaCode = cursor.fetchall()[0][0]

            cursor.execute("INSERT INTO OperatingAreas VALUES (?, ?)", areaCode, ngoID)
            connection.commit()
            connection.close()
            self.close()