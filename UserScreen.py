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

        self.SearchButton.clicked.connect(lambda: self.Search(userID))
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

        cursor.execute("""select NGO.name, Project.projectName, Donation.amount, donation.donationDateTime
                       from Users join Donation on Donation.userID=Users.userID 
                       join Project on Project.projectID=Donation.projectID
                       join NGO on NGO.ngoID=Project.ngoID
                       where Users.userID=?
                       """, userID)
        data=cursor.fetchall()
        rows=len(data)
        cols=len(data[0])
        for col_index in range(cols):
            self.tableWidget.setColumnWidth(3, 200)

        self.tableWidget.setRowCount(rows)
        self.tableWidget.setColumnCount(cols)
        for row_index, row_data in enumerate(data):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.tableWidget.setItem(row_index, col_index, item)
        self.tableWidget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)



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

    def Search(self, userID):
        
        if self.checkBox_2.isChecked():
            selected_project=self.comboBox_3.currentText()
            server = 'SABIR\SQLEXPRESS'
            database = 'NGOConnect'  # Name of your NGOConnect database
            connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')

            cursor = connection.cursor()
            #load all areas in comboBox_5
            cursor.execute("select ngoID from project where projectName=?", selected_project)
            ngo_ID=cursor.fetchall()[0][0]
            cursor.execute("select projectID from project where projectName=?", selected_project)
            project_ID=cursor.fetchall()[0][0]
            cursor.execute("select name from NGO where ngoID=?", ngo_ID)
            ngo_Name=cursor.fetchall()[0][0]
            cursor.execute("select getdate()")
            donationDateTime=cursor.fetchall()[0][0]
            print(ngo_Name, ngo_ID, userID, donationDateTime)
            self.comboBox_5.clear()
            self.ProjectPage = ProjectDetails(project_ID, ngo_Name, ngo_ID, userID, donationDateTime)
            self.ProjectPage.show()
            self.ProjectPage.DonateButton.clicked.connect(lambda: self.loadData(userID))
            
        else:
            if self.checkBox_3.isChecked() or self.checkBox_4.isChecked():
                self.NGOList = NGOs()
                self.NGOList.show()
            else:
                if self.checkBox.isChecked():
                    selected_NGO=self.comboBox_2.currentText()
                    self.NGOPage = NGODetails(selected_NGO, userID)
                    self.NGOPage.show()
                    self.NGOPage.ShowProject.destroyed.connect(lambda: self.loadData(userID))


    
 
            
        