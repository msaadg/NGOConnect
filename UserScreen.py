from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
import Screens

from UserSearchNGO import NGODetails
from UserSearchNGO import ProjectDetails
from UserSearchNGO import NGOs

class UserData(QtWidgets.QMainWindow):  
    def __init__(self, userID):
        super().__init__()

        uic.loadUi('Screens/UserPage.ui', self)  #Screens/UserSignUp.ui
        self.setWindowTitle("User screen")
        self.userName.setDisabled(True)
        self.userEmail.setDisabled(True)
        self.loadData(userID)

        self.SearchButton.clicked.connect(self.Search)
        self.checkBox_2.stateChanged.connect(self.ProjectSearch)
        self.checkBox.stateChanged.connect(self.NGOSearch)
        self.checkBox_3.stateChanged.connect(self.CategorySearch)
        self.checkBox_4.stateChanged.connect(self.AreaSearch)

    def loadData(self, userID):
        server = 'SABIR\SQLEXPRESS'
        database = 'NGOConnect' 
        connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')
        
        cursor=connection.cursor()
        cursor.execute("SELECT userEmail, userName FROM Users WHERE userID = ?", userID)
        userData = cursor.fetchall()[0]
        self.userName.setText(userData[1])
        self.userEmail.setText(userData[0])
        connection.close()

    def ProjectSearch(self):
        if self.checkBox_2.isChecked() :
            self.comboBox_3.setEnabled(True)
            server = 'SABIR\SQLEXPRESS'
            database = 'NGOConnect'  # Name of your NGOConnect database
            use_windows_authentication = True 
            connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')

            cursor = connection.cursor()
            #load all projects in comboBox_3
            cursor.execute("SELECT projectName FROM Project")
            self.comboBox_3.clear()
            self.comboBox_3.addItem("")
            for row in cursor.fetchall():
                self.comboBox_3.addItem(row[0])
            connection.close()
        else:
            self.comboBox_3.setEnabled(False)


    def NGOSearch(self):
        if self.checkBox.isChecked() :
            self.comboBox_2.setEnabled(True)
            server = 'SABIR\SQLEXPRESS'
            database = 'NGOConnect'  # Name of your NGOConnect database
            use_windows_authentication = True 
            connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')

            cursor = connection.cursor()
            #load all NJO name in comboBox_2
            cursor.execute("SELECT name FROM NGO")
            self.comboBox_2.clear()
            self.comboBox_2.addItem("")
            for row in cursor.fetchall():
                self.comboBox_2.addItem(row[0])
            connection.close()
        else:
            self.comboBox_2.setEnabled(False)

    def CategorySearch(self):
        if self.checkBox_3.isChecked() :
            self.comboBox_4.setEnabled(True)
            server = 'SABIR\SQLEXPRESS'
            database = 'NGOConnect'  # Name of your NGOConnect database
            use_windows_authentication = True 
            connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')

            cursor = connection.cursor()
            #load all categories in comboBox_4
            cursor.execute("SELECT categoryName FROM category")
            self.comboBox_4.clear()
            self.comboBox_4.addItem("")
            for row in cursor.fetchall():
                self.comboBox_4.addItem(row[0])
            connection.close()
        else:
            self.comboBox_4.setEnabled(False)

    def AreaSearch(self):
        if self.checkBox_4.isChecked() :
            self.comboBox_5.setEnabled(True)
            server = 'SABIR\SQLEXPRESS'
            database = 'NGOConnect'  # Name of your NGOConnect database
            use_windows_authentication = True 
            connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')

            cursor = connection.cursor()
            #load all areas in comboBox_5
            cursor.execute("SELECT areaName FROM Area")
            self.comboBox_5.clear()
            self.comboBox_5.addItem("")
            for row in cursor.fetchall():
                self.comboBox_5.addItem(row[0])
            connection.close()

        else:
            self.comboBox_5.setEnabled(False)

    def Search(self):
        if self.checkBox_2.isChecked():
            selected_project=self.comboBox_3.currentText()
            self.ProjectPage = ProjectDetails(selected_project)
            self.ProjectPage.show()
             

        else:
            if self.checkBox_3.isChecked() or self.checkBox_4.isChecked():
                self.NGOList = NGOs()
                self.NGOList.show()
            else:
                if self.checkBox.isChecked():
                    self.NGOPage = NGODetails()
                    self.NGOPage.show()
            
        