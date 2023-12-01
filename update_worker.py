from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

class UpdateWorker(QtWidgets.QMainWindow):
    def __init__(self, workerEmail):
        super().__init__()
        uic.loadUi('Screens/UpdateWorker.ui',self)

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
        cursor.execute("SELECT workerID FROM Worker WHERE workerEmail = ?", workerEmail)
        workerID = cursor.fetchall()[0][0]
        connection.close()

        self.loadData(workerID)
        self.updateWorkerDoneBtn.clicked.connect(lambda: self.WorkerUpdated(workerID))
        self.updateWorkerCancelBtn.clicked.connect(lambda: self.close())

    def loadData(self, workerID):
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
        cursor.execute("SELECT workerEmail, workerName, gender, age FROM Worker WHERE workerID = ?", workerID)

        workerDetails = cursor.fetchall()[0]
        self.workerEmail.setText(workerDetails[0])
        self.workerName.setText(workerDetails[1])
        self.workerGender.setText(workerDetails[2])
        self.workerAge.setText(str(workerDetails[3]))

        connection.close()

    def WorkerUpdated(self, workerID):
        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Worker Details Successfully Updated")
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Ok:
            workerName = self.workerName.text()
            workerEmail = self.workerEmail.text()
            workerGender = self.workerGender.text()
            workerAge = self.workerAge.text()

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

            update_query = """
                UPDATE Worker
                SET workerEmail = ?, workerName = ?, gender = ?, age = ?
                WHERE workerID = ?
            """

            cursor.execute(update_query, workerEmail, workerName, workerGender, workerAge, workerID)
            connection.commit()
            connection.close()
            self.close()