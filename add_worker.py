from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

class AddWorker(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Screens/AddWorker.ui',self)
        self.addWorkerDoneBtn.clicked.connect(self.WorkerAdded)
        self.workerPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def WorkerAdded(self):
        connection = pyodbc.connect(
                'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
        )
        
        # server = 'SABIR\SQLEXPRESS'
        # database = 'NGOConnect'  # Name of your NGOConnect database
        # use_windows_authentication = True 
        # connection = pyodbc.connect(
        # )

        cursor = connection.cursor()
        insert_query1 = """
            INSERT INTO Worker
            ([ngoID], [workerEmail], [workerName], [workerPassword], [gender], [age])
            VALUES (?, ?, ?, ?, ?, ?)
        """

        insert_query2 = """
            INSERT INTO WorkerProject
            ([workerID], [projectID], [workerStatus])
            VALUES (?, ?, ?)
        """

        cursor.execute(insert_query1, (1, self.workerEmail.text(), self.workerName.text(), self.workerPassword.text(), 
                                      self.gender.text(), int(self.age.text())))
        
        cursor.execute(insert_query2, (cursor.execute("SELECT IDENT_CURRENT('Worker')").fetchone()[0], 1, "Active"))
        
        connection.commit()
        connection.close()


        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Worker Is Successfully Added")
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Ok:
            self.close()

