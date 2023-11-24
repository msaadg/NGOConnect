from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

class UserLogin(QtWidgets.QMainWindow):  
    def __init__(self):
        super().__init__()
        uic.loadUi('Screens/UserLogin.ui', self)

        self.userPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.userLoginBtn.clicked.connect(self.ShowUser)


    def ShowUser(self):
        userEmail = self.userEmail.text()
        userPassword = self.userPassword.text()

        connection = pyodbc.connect(
                'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
        )

        # server = 'SABIR\SQLEXPRESS'
        # database = 'NGOConnect'  # Name of your NGOConnect database
        # use_windows_authentication = True 
        # connection = pyodbc.connect(
        #         'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
        # )

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
                x += 1
                # TODO: show NGO page

                # self.view_userpage = UserPage()
                # self.view_userpage.show()
                # self.close()
            else:
                Dialog = QtWidgets.QMessageBox()
                Dialog.setWindowTitle("Error")
                Dialog.setText("Incorrect Password")
                Dialog.exec()