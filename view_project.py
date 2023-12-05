from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

from worker_to_project import WorkerToProject
from update_worker import UpdateWorker

class ViewProject(QtWidgets.QMainWindow):
    def __init__(self, projectID):
        # Call the inherited classes __init__ method
        super().__init__()

        # Load the .ui file
        uic.loadUi('Screens/ViewProject.ui', self)
        self.setWindowTitle("Project Details")

        self.ngoName.setDisabled(True)
        self.projectName.setDisabled(True)
        self.projectScale.setDisabled(True)
        self.projectStartDate.setDisabled(True)
        self.projectEndDate.setDisabled(True)
        self.projectSaveBtn.setDisabled(True)

        self.totalAmount.setDisabled(True)


        self.addWorkerBtn.clicked.connect(lambda: self.addWorker(projectID))
        self.removeWorkerBtn.clicked.connect(lambda: self.removeWorker(projectID))
        self.projectEditBtn.clicked.connect(self.editProject)
        self.projectSaveBtn.clicked.connect(lambda: self.saveProject(projectID))
        self.endProjectBtn.clicked.connect(lambda: self.endProject(projectID))

        self.donationSearchBtn.clicked.connect(lambda: self.searchDonation(projectID))  

        self.loadProjectData(projectID)
        self.loadDonationData(projectID)

    def refreshData(self, projectID):
        self.loadProjectData(projectID)
        self.loadDonationData(projectID)

    def loadDonationData(self, projectID):
        connection = pyodbc.connect(
                'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
        )

        # server = 'SABIR\SQLEXPRESS'
        # database = 'NGOConnect'  # Name of your NGOConnect database 
        # connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')

        cursor = connection.cursor()

        select_query = """
            SELECT u.userName, d.amount, d.donationDateTime
            FROM Users u, Donation d
            WHERE u.userID = d.userID and d.projectID = ?
        """

        header = self.donationDetails.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        self.donationDetails.clearContents()
        self.donationDetails.setRowCount(0)

        cursor.execute(select_query, projectID)
        # columns are Name, Amount, Time, and Date in donationDetails
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.donationDetails.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                if col_index == 2:
                    date_time = str(cell_data).split(" ")
                    date = QTableWidgetItem(date_time[0])
                    time = QTableWidgetItem(date_time[1])
                    self.donationDetails.setItem(row_index, col_index, time)
                    self.donationDetails.setItem(row_index, col_index + 1, date)
                    self.donationDetails.item(row_index, col_index).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.donationDetails.item(row_index, col_index + 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                else:
                    item = QTableWidgetItem(str(cell_data))
                    self.donationDetails.setItem(row_index, col_index, item)
                    self.donationDetails.item(row_index, col_index).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Close the database connection
        connection.close()

        # sum the column of amount
        total = 0
        for row in range(self.donationDetails.rowCount()):
            total += float(self.donationDetails.item(row, 1).text())
        self.totalAmount.setText(str(total))


    def searchDonation(self, projectID):
        self.loadDonationData(projectID)

        # get date from startDate dateEdit
        if self.startDate.date() == QDate(2000, 1, 1):
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Please Set Start Date Greater Than 2000-01-01")
            Dialog.exec()
            return
        
        # check if startDate is greater than endDate
        if self.startDate.date() > self.endDate.date():
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Start Date Cannot Be Greater Than End Date")
            Dialog.exec()
            return
        
        # check if startDate is greater than current date
        if self.startDate.date() > QDate.currentDate():
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Start Date Cannot Be Greater Than Current Date")
            Dialog.exec()
            return
        
        # check if endDate is greater than current date
        if self.endDate.date() > QDate.currentDate():
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("End Date Cannot Be Greater Than Current Date")
            Dialog.exec()
            return
        
        for row in range(self.donationDetails.rowCount() - 1, -1, -1):
            if self.donationDetails.item(row, 3).text() < self.startDate.date().toString("yyyy-MM-dd") or self.donationDetails.item(row, 3).text() > self.endDate.date().toString("yyyy-MM-dd"):
                self.donationDetails.removeRow(row)

        if self.donorName.text() != "":
            for row in range(self.donationDetails.rowCount() - 1, -1, -1):
                if self.donationDetails.item(row, 0).text() != self.donorName.text():
                    self.donationDetails.removeRow(row)

        # sum the column of amount
        total = 0
        for row in range(self.donationDetails.rowCount()):
            total += float(self.donationDetails.item(row, 1).text())
        self.totalAmount.setText(str(total))


    def loadProjectData(self, projectID):
        connection = pyodbc.connect(
                'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
        )

        # server = 'SABIR\SQLEXPRESS'
        # database = 'NGOConnect'  # Name of your NGOConnect database 
        # connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')


        cursor = connection.cursor()

        select_query = """
            SELECT n.name, p.projectName, p.scale, p.startDate, p.endDate
            FROM NGO n, Project p
            WHERE n.ngoID = p.ngoID and p.projectID = ?    
        """
        cursor.execute(select_query, projectID)
        projectDetails = cursor.fetchall()[0]

        self.ngoName.setText(projectDetails[0])
        self.projectName.setText(projectDetails[1])
        self.projectScale.setText(str(projectDetails[2]))
        self.projectStartDate.setDate(projectDetails[3])
        if projectDetails[4] == None:
            self.projectEndDate.setText(" -")
        else:
            #convert datetime to sting
            self.projectEndDate.setText(projectDetails[4].strftime("%Y-%m-%d"))
            self.endProjectBtn.setDisabled(True)


        self.projectName.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)


        select_query = """
            SELECT w.workerEmail, w.workerName, w.gender, w.age
            FROM Worker w, WorkerProject wp
            WHERE w.workerID = wp.workerID and wp.projectID = ?
        """

        header = self.workerDetails.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        self.workerDetails.clearContents()
        self.workerDetails.setRowCount(0)
        
        cursor.execute(select_query, projectID)
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.workerDetails.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.workerDetails.setItem(row_index, col_index, item)
                self.workerDetails.item(row_index, col_index).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Close the database connection
        connection.close()

    def addWorker(self, projectID):
        self.add_worker = WorkerToProject(projectID)
        self.add_worker.show()
        self.add_worker.addWorkerDoneBtn.clicked.connect(lambda: self.refreshData(projectID))

    def removeWorker(self, projectID):
        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Are You Sure You Want To Remove This Worker?")
        Dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Yes:
            # do the delete procedure of project
            workerEmail = self.workerDetails.item(self.workerDetails.currentRow(), 0).text()
            connection = pyodbc.connect(
                    'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
            )

            # server = 'SABIR\SQLEXPRESS'
            # database = 'NGOConnect'  # Name of your NGOConnect database 
            # connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')

            
            cursor = connection.cursor()
            cursor.execute("SELECT workerID FROM Worker WHERE workerEmail = ?", workerEmail)
            workerID = cursor.fetchall()[0][0]

            delete_query = """
                DELETE FROM WorkerProject
                WHERE workerID = ? and projectID = ?
            """
            cursor.execute(delete_query, workerID, projectID)
            connection.commit()
            connection.close()
            self.refreshData(projectID)

    def editProject(self):
        self.projectName.setDisabled(False)
        self.projectScale.setDisabled(False)
        self.projectStartDate.setDisabled(False)

        self.projectSaveBtn.setDisabled(False)

        self.projectEditBtn.setText("Cancel")
        self.projectEditBtn.clicked.connect(self.cancelEdit)

        self.endProjectBtn.setDisabled(True)

    def cancelEdit(self):
        self.projectName.setDisabled(True)
        self.projectScale.setDisabled(True)
        self.projectStartDate.setDisabled(True)

        self.projectSaveBtn.setDisabled(True)

        self.projectEditBtn.setText("Edit")
        self.projectEditBtn.clicked.connect(self.editProject)

        if self.projectEndDate.text() == " -":
            self.endProjectBtn.setDisabled(False)
        else:
            self.endProjectBtn.setDisabled(True)

    def saveProject(self, projectID):
        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Are You Sure You Want To Save The Changes?")
        Dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Yes:
            projectName = self.projectName.text()
            projectScale = self.projectScale.text()
            projectStartDate = self.projectStartDate.date().toString("yyyy-MM-dd")

            connection = pyodbc.connect(
                    'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
            )

            # server = 'SABIR\SQLEXPRESS'
            # database = 'NGOConnect'  # Name of your NGOConnect database 
            # connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')

            
            cursor = connection.cursor()
            cursor.execute("UPDATE Project SET projectName = ?, scale = ?, startDate = ? WHERE projectID = ?", projectName, projectScale, projectStartDate, projectID)
            connection.commit()
            connection.close()

            self.projectName.setDisabled(True)
            self.projectScale.setDisabled(True)
            self.projectStartDate.setDisabled(True)

            self.projectSaveBtn.setDisabled(True)

            self.projectEditBtn.setText("Edit")
            self.projectEditBtn.clicked.connect(self.editProject)

    def endProject(self, projectID):
        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Are You Sure You Want To End This Project?")
        Dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Yes:
            connection = pyodbc.connect(
                    'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
            )

            # server = 'SABIR\SQLEXPRESS'
            # database = 'NGOConnect'  # Name of your NGOConnect database 
            # connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')

            
            cursor = connection.cursor()
            cursor.execute("UPDATE Project SET endDate = ? WHERE projectID = ?", QDate.currentDate().toString("yyyy-MM-dd"), projectID)
            connection.commit()
            connection.close()

            self.projectEndDate.setText(QDate.currentDate().toString("yyyy-MM-dd"))

            self.endProjectBtn.setDisabled(True)