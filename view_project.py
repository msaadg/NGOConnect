from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

from worker_to_project import WorkerToProject
from update_worker import UpdateWorker

class ViewProject(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super().__init__()

        # Load the .ui file
        uic.loadUi('Screens/ViewProject.ui', self)

        self.loadProjectData()
        # self.refreshWorkerTable()
        self.addWorkerBtn.clicked.connect(self.addWorker)
        # self.removeWorkerBtn.clicked.connect(self.removeWorker)
        # self.updateBtn.clicked.connect(self.updateWorker)

        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.refreshWorkerTable)
        # self.timer.start(5000)

    def refreshWorkerTable(self):
        self.workerDetails.clearContents()
        self.workerDetails.setRowCount(0)
        self.populateWorkerTable()


    def populateWorkerTable(self):
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

        # TODO: Write SQL query to fetch Workers Data
        select_query = "SELECT workerID, workerEmail, workerName, gender, age from Worker where workerID in (select workerID from WorkerProject where projectID = 1)"
        cursor.execute(select_query)

        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.workerDetails.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.workerDetails.setItem(row_index, col_index, item)

        # Close the database connection
        connection.close()

        # Adjust content display
        header = self.workerDetails.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

    def loadProjectData(self):
        self.setWindowTitle("Project")

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

        select_query = "SELECT projectID, name, projectName, scale, startDate from Project p, NGO n where p.ngoID = n.ngoID and projectID = 1"
        cursor.execute(select_query)

        # fill line edits
        for row in cursor:
            self.projectID.setText(str(row[0]))
            self.ngoName.setText(str(row[1]))
            self.projectName.setText(str(row[2]))
            self.scale.setText(str(row[3]))
            self.startDate.setDate(QDate.fromString(str(row[4]), "yyyy-MM-dd"))

        # set projectName to centre of line edit
        self.projectName.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # disable editing of projectID, ngoID, projectName, scale, startDate
        self.projectID.setDisabled(True)
        self.ngoName.setDisabled(True)
        self.projectName.setDisabled(True)
        self.scale.setDisabled(True)
        self.startDate.setDisabled(True)

        # Close the database connection
        connection.close()

    def addWorker(self):
        self.add_worker = WorkerToProject()
        self.add_worker.show()
        # self.add_worker.addWorkerDoneBtn.clicked.connect(self.refreshWorkerTable)


    def updateWorker(self):
        workerDetails = []
        for i in range(0, 5):
            workerDetails.append(self.workerDetails.item(self.workerDetails.currentRow(), i).text())

        self.update_worker = UpdateWorker(workerDetails)
        self.update_worker.show()
        self.update_worker.updateWorkerDoneBtn.clicked.connect(self.refreshWorkerTable)

    def removeWorker(self):
        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Are You Sure You Want To Remove This Worker?")
        Dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        Option = Dialog.exec()
        x = 0
        if Option == QtWidgets.QMessageBox.StandardButton.Yes:
            # do the delete procedure of project
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
            delete_query1 = """
                DELETE FROM WorkerProject
                WHERE workerID = ? and projectID = ?
            """

            delete_query2 = """
                DELETE FROM Worker
                WHERE workerID = ? and ngoID = ?
            """

            cursor.execute(delete_query1, (int(self.workerDetails.item(self.workerDetails.currentRow(), 0).text()), 1))
            cursor.execute(delete_query2, (int(self.workerDetails.item(self.workerDetails.currentRow(), 0).text()), 1))
            
            connection.commit()
            connection.close()
            self.refreshWorkerTable()

