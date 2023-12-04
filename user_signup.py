from PyQt6 import QtWidgets, uic, QtCore , QtGui
from PyQt6.QtCore import QDate, QTimer 
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
import re

class UserSignup(QtWidgets.QMainWindow):  
    def __init__(self):
        super().__init__()

        uic.loadUi('Screens/UserSignUp.ui', self)


        self.userSignupBtn.clicked.connect(self.UserCreate)

        self.userPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.userConfirmPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def UserCreate(self):
        userName = self.userName.text()
        userEmail = self.userEmail.text()
        userPassword = self.userPassword.text()
        userConfirmPassword = self.userConfirmPassword.text()

        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        # connection = pyodbc.connect(
        #         'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
        # )

        server = 'SABIR\SQLEXPRESS'
        database = 'NGOConnect'  # Name of your NGOConnect datab
        connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')


        cursor = connection.cursor()
        cursor.execute("SELECT userEmail FROM Users")
        userEmails = [x[0] for x in cursor.fetchall()]

        if userName == "" or userEmail == "" or userPassword == "" or userConfirmPassword == "":
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Please Fill All The Fields")
            Option = Dialog.exec()
            return
        
        # validate email using regex
        elif not re.search(regex, userEmail):
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Invalid Email")
            Option = Dialog.exec()
            return
        
        # check if email already exits in database
        elif userEmail in userEmails:
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Email Already Exists \n Try Another Email")
            Option = Dialog.exec()
            return
        
        elif len(userPassword) < 8:
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Password Must Be At Least 8 Characters Long")
            Option = Dialog.exec()
            return

        elif userPassword != userConfirmPassword:
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Passwords Don't Match")
            Option = Dialog.exec()
            return
        
        else:
            insert_query = """  
                INSERT INTO Users (userEmail, userName, userPassword)
                VALUES (?, ?, ?)
            """
            cursor.execute(insert_query, (userEmail, userName, userPassword))
            connection.commit()

            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Success")
            Dialog.setText("User Created Successfully!")
            Dialog.exec()
            self.close()

        connection.close()
