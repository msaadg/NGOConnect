from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
import re

class AddWorker(QtWidgets.QMainWindow):
    def __init__(self, ngoID):
        super().__init__()
        uic.loadUi('Screens/AddWorker.ui',self)


        self.addWorkerDoneBtn.clicked.connect(lambda: self.WorkerAdded(ngoID))
        self.addWorkerCancelBtn.clicked.connect(lambda: self.close())
        self.workerPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def WorkerAdded(self, ngoID):
        workerName = self.workerName.text()
        workerEmail = self.workerEmail.text()
        workerPassword = self.workerPassword.text()
        workerGender = self.workerGender.currentText()
        workerAge = self.workerAge.text()

        if workerName == "" or workerEmail == "" or workerPassword == "" or workerGender == "" or workerAge == "":
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Please Fill All The Fields")
            Dialog.exec()
            return

        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
        )
        
        # server = 'SABIR\SQLEXPRESS'
        # database = 'NGOConnect'  # Name of your NGOConnect database
        # use_windows_authentication = True 
        # connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')

        cursor = connection.cursor()

        #check whether workerEmail already exists
        cursor.execute("SELECT workerEmail FROM Worker")
        workerEmails = [x[0] for x in cursor.fetchall()]

        if workerEmail in workerEmails:
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Email Already Exists \n Try Another Email")
            Dialog.exec()
            return
        
        elif not re.search(regex, workerEmail):
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Invalid Email")
            Option = Dialog.exec()
            return
        
        elif not workerAge.isdigit():
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Invalid Age")
            Option = Dialog.exec()
            return
        
        elif int(workerAge) < 18:
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Age Must Be Greater Than 18")
            Option = Dialog.exec()
            return
        
        elif int(workerAge) > 100:
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Age Must Be Less Than 100")
            Option = Dialog.exec()
            return

        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Worker Is Successfully Added")
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Ok:
            insert_query = """
                INSERT INTO Worker (ngoID, workerEmail, workerName, workerPassword, gender, age, dateAdded)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """

            cursor.execute(insert_query, (ngoID, workerEmail, workerName, workerPassword, workerGender, workerAge, QDate.currentDate().toString(QtCore.Qt.DateFormat.ISODate)))
            connection.commit()


            connection.commit()
            connection.close()
            self.close()

