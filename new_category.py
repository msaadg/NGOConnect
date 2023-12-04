from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QSortFilterProxyModel
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
import pyodbc

class NewCategory(QtWidgets.QMainWindow):
    def __init__(self, ngoID):
        super().__init__()
        uic.loadUi('Screens/NGONewCategory.ui' , self)

        #set window title
        self.setWindowTitle("Add New Category")

        self.model = QStandardItemModel(self.categories)
        self.proxyModel = QSortFilterProxyModel(self.categories)
        self.proxyModel.setSourceModel(self.model)
        self.categories.setModel(self.proxyModel)

        self.categories.setEditable(True)
        self.categories.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.NoInsert)
        self.categories.completer().setCompletionMode(QtWidgets.QCompleter.CompletionMode.PopupCompletion)
        self.categories.completer().setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        self.categories.lineEdit().textEdited.connect(self.proxyModel.setFilterFixedString)

        self.categoryDoneBtn.clicked.connect(lambda: self.AddCategory(ngoID))
        self.categoryCancelBtn.clicked.connect(lambda: self.close())
        
        self.loadCategories(ngoID)

        self.categories.setCurrentIndex(-1)

    
    def loadCategories(self, ngoID):
        # load data into catgeories combo box
        # connection = pyodbc.connect(
        #         'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
        # )

        server = 'SABIR\SQLEXPRESS'
        database = 'NGOConnect'  # Name of your NGOConnect databas 
        connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')

        cursor = connection.cursor()

        # only get those categories which are not currently assigned to the NGO
        cursor.execute("""
            SELECT c.categoryName
            FROM Category c
            WHERE c.categoryName NOT IN (
                SELECT oc.categoryName
                FROM OperatingCategories oc
                WHERE oc.ngoID = ?
            )
        """, ngoID)
        categories = cursor.fetchall()

        for category in categories:
            item = QStandardItem(category[0])
            self.model.appendRow(item)

        connection.close()

    
    def AddCategory(self, ngoID):
        selectedCategory = self.categories.currentText()
        if selectedCategory == "":
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Please Select A Category")
            Dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            Dialog.exec()
            return

        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Are You Sure You Want To Add This Category?")
        Dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Yes:
            # connection = pyodbc.connect(
            #         'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
            # )

            server = 'SABIR\SQLEXPRESS'
            database = 'NGOConnect'  # Name of your NGOConnect database 
            connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')

            cursor = connection.cursor()

            categoryName = self.categories.currentText()
            cursor.execute("INSERT INTO OperatingCategories VALUES (?, ?)", ngoID, categoryName)

            connection.commit()

            self.close()

        # self.refreshData(ngoID)