from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

from add_worker import AddWorker
from update_worker import UpdateWorker

class WorkerData(QtWidgets.QMainWindow):
    def __init__(self, ngoID):
        super().__init__()
        uic.loadUi('Screens/WorkerPage.ui' , self)

        #set windows title
        self.setWindowTitle("Worker Data")

        self.addWorkerBtn.clicked.connect(lambda: self.AddWorker(ngoID))
        self.removeWorkerBtn.clicked.connect(lambda: self.removeWorker(ngoID))
        self.updateWorkerBtn.clicked.connect(lambda: self.UpdateWorker(ngoID))

        self.loadData(ngoID)

    def refreshData(self, ngoID):
        self.loadData(ngoID)

    def loadData(self, ngoID):
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

        header = self.workerDetails.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        self.workerDetails.clearContents()
        self.workerDetails.setRowCount(0)

        cursor.execute("SELECT workerEmail, workerName, gender, age FROM Worker WHERE ngoID = ?", ngoID)
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.workerDetails.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.workerDetails.setItem(row_index, col_index, item)
                self.workerDetails.item(row_index, col_index).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        connection.close()
    

    def AddWorker(self, ngoID):
        self.new_worker = AddWorker(ngoID)
        self.new_worker.show()
        self.new_worker.addWorkerDoneBtn.clicked.connect(lambda: self.refreshData(ngoID))


    def UpdateWorker(self, ngoID):
        workerEmail = self.workerDetails.item(self.workerDetails.currentRow(), 0).text()
        self.worker_update = UpdateWorker(workerEmail)
        self.worker_update.show()
        self.worker_update.updateWorkerDoneBtn.clicked.connect(lambda: self.refreshData(ngoID))

    def removeWorker(self, ngoID):
        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Are You Sure You Want To Remove This Worker?")
        Dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Yes:
            workerEmail = self.workerDetails.item(self.workerDetails.currentRow(), 0).text()
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
            workerID = cursor.fetchone()[0]

            delete_query1 = """
                DELETE FROM WorkerProject
                WHERE workerID = ?
            """

            delete_query2 = """
                DELETE FROM Worker
                WHERE workerID = ?
            """

            cursor.execute(delete_query1, workerID)
            cursor.execute(delete_query2, workerID)

            connection.commit()
            connection.close()

            self.refreshData(ngoID)