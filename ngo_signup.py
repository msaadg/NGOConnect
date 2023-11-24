from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
import re

class NGOSignup(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Screens/NGOSignUp.ui' , self)

        self.ngoSignupBtn.clicked.connect(self.NGOCreate)

        # set Password and Confirm Password to hidden
        self.ngoPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.ngoConfirmPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def NGOCreate(self):
        ngoName = self.ngoName.text()
        ngoAddress = self.ngoAddress.text()
        ngoEmail = self.ngoEmail.text()
        ngoPassword = self.ngoPassword.text()
        ngoConfirmPassword = self.ngoConfirmPassword.text()

        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
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
        cursor.execute("SELECT ngoEmail FROM NGO")
        ngoEmails = [x[0] for x in cursor.fetchall()]

        if ngoName == "" or ngoAddress == "" or ngoEmail == "" or ngoPassword == "" or ngoConfirmPassword == "":
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Please Fill All The Fields")
            Option = Dialog.exec()
            return
        
        # validate email using regex
        elif not re.search(regex, ngoEmail):
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Invalid Email")
            Option = Dialog.exec()
            return
        
        # check if email already exits in database
        elif ngoEmail in ngoEmails:
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Email Already Exists \n Try Another Email")
            Option = Dialog.exec()
            return
        
        elif len(ngoPassword) < 8:
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Password Should Be Atleast 8 Characters Long")
            Option = Dialog.exec()
            return
    
        elif ngoPassword != ngoConfirmPassword:
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Password And Confirm Password Are Not Same")
            Option = Dialog.exec()
            return
        
        else:
            insert_query = """
                INSERT INTO NGO(name, regDate, address, ngoEmail, ngoPassword)
                VALUES(?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, (ngoName, QDate.currentDate().toString("yyyy-MM-dd"), ngoAddress, ngoEmail, ngoPassword))
            connection.commit()        

            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Success")
            Dialog.setText("Your NGO Is Successfully Added To The Database!")
            Dialog.exec()
            self.close()

        # Close the database connection
        connection.close()