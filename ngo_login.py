from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

from ngo_page import NGOPage

class NGOLogin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Screens/NGOLogin.ui' , self)


        self.ngoPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.ngoLoginBtn.clicked.connect(self.ShowNGO)


    def ShowNGO(self):
        ngoEmail = self.ngoEmail.text()
        ngoPassword = self.ngoPassword.text()

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
        cursor.execute("SELECT ngoEmail FROM NGO")
        ngoEmails = [x[0] for  x in cursor.fetchall()]

        if ngoEmail == "" or ngoPassword == "":
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Please Fill All The Fields")
            Dialog.exec()

        elif ngoEmail not in ngoEmails:
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Email Does Not Exist")
            Dialog.exec()
        
        elif ngoEmail in ngoEmails:
            cursor.execute("SELECT ngoPassword FROM NGO WHERE ngoEmail = ?", ngoEmail)
            ngoRealPassword = cursor.fetchall()[0][0]
            if ngoPassword == ngoRealPassword:
                # show NGO page
                self.view_ngopage = NGOPage()
                self.view_ngopage.show()
                self.close()
            else:
                Dialog = QtWidgets.QMessageBox()
                Dialog.setWindowTitle("Error")
                Dialog.setText("Incorrect Password")
                Dialog.exec()
