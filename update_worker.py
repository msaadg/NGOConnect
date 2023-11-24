from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

class UpdateWorker(QtWidgets.QMainWindow):
    def __init__(self, workerDetails):
        super().__init__()
        uic.loadUi('Screens/UpdateWorker.ui',self)
        #set window title
        self.setWindowTitle("Update Worker")
        self.workerEmail.setText(workerDetails[1])
        self.workerName.setText(workerDetails[2])
        self.gender.setText(workerDetails[3])
        self.age.setText(workerDetails[4])

        self.updateWorkerDoneBtn.clicked.connect(lambda: self.WorkerUpdated(workerDetails))

    def WorkerUpdated(self, workerDetails):
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

        cursor.execute(update_query, (
            self.workerEmail.text(),
            self.workerName.text(),
            self.gender.text(),
            int(self.age.text()),
            workerDetails[0]  # This is the workerID from the workerDetails list
        ))
        
        connection.commit()
        connection.close()

        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Worker Details Successfully Updated")
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Ok:
            self.close()
