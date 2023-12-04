from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

from UserScreen import UserData

class UserLogin(QtWidgets.QMainWindow):  
    def __init__(self):
        super().__init__()
        uic.loadUi('Screens/UserLogin.ui', self)

        self.userPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.userLoginBtn.clicked.connect(self.ShowUser)


    def ShowUser(self):

        # self.user_page = UserData()
        # self.user_page.show()
        # self.close()
        userEmail = self.userEmail.text()
        userPassword = self.userPassword.text()

        # connection = pyodbc.connect(
        #         'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
        # )

        server = 'SABIR\SQLEXPRESS'
        database = 'NGOConnect'  # Name of your NGOConnect datab
        connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')


        cursor = connection.cursor()

        # get all emails 
        cursor.execute("SELECT userEmail FROM Users")
        userEmails = [x[0] for x in cursor.fetchall()]

        if userEmail == "" or userPassword == "":
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Please Fill All The Fields")
            Dialog.exec()

        elif userEmail not in userEmails:
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Email Does Not Exist")
            Dialog.exec()

        elif userEmail in userEmails:
            cursor.execute("SELECT userPassword FROM Users WHERE userEmail = ?", userEmail)
            userRealPassword = cursor.fetchall()[0][0]
            if userPassword == userRealPassword:
                cursor.execute("SELECT userID FROM users WHERE userEmail = ?", userEmail)
                userID = cursor.fetchall()[0][0]
                self.user_page = UserData(userID)
                self.user_page.show()
                self.close()
                
            else:
                Dialog = QtWidgets.QMessageBox()
                Dialog.setWindowTitle("Error")
                Dialog.setText("Incorrect Password")
                Dialog.exec()