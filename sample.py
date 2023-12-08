# Database:

# NGO {
# 	ngoID int pk increments
# 	name varchar
# 	regDate date
# 	address varchar
# }

# Project {
# 	projectID int pk increments
# 	ngoID int *> NGO.ngoID
# 	projectName varchar
# 	scale int
# 	startDate date
# 	endDate date null
# }

# User {
# 	userID int pk increments
# 	userEmail varchar
# 	userName varchar
# 	userPassword varchar
# }

# Category {
# 	categoryName varchar pk
# }

# SavedProject {
# 	projectID int pk *> Project.projectID
# 	userID int pk *> User.userID
# }

# DonatedProject {
# 	projectID int pk *> Project.projectID
# 	userID int pk *> User.userID
# }

# OperatingCategories {
# 	ngoID int pk *> NGO.ngoID
# 	categoryName varchar pk *> Category.categoryName
# }

# Area {
# 	areaCode int pk increments
# 	areaName varchar
# 	city varchar
# 	country varchar
# }

# OperatingAreas {
# 	areaCode int pk *> Area.areaCode
# 	ngoID int pk *> NGO.ngoID
# }

# Worker {
# 	workerID int pk increments
# 	ngoID int *> NGO.ngoID
# 	workerEmail varchar
# 	workerName varchar
# 	workerPassword varchar
# 	gender varchar
# 	age int
# }

# WorkerProject {
# 	workerID int pk *> Worker.workerID
# 	projectID int pk *> Project.projectID
# 	workerStatus varchar
# }




# Importing essential modules
from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

# Main Window Class
class UI(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(UI, self).__init__()

        # Load the .ui file
        uic.loadUi('ViewProject.ui', self)

        self.loadProjectData()
        self.refreshWorkerTable()
        self.addWorkerBtn.clicked.connect(self.addWorker)
        self.removeWorkerBtn.clicked.connect(self.removeWorker)
        self.updateBtn.clicked.connect(self.updateWorker)

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

        cursor = connection.cursor()

        select_query = "SELECT projectID, ngoID, projectName, scale, startDate from Project where projectID = 1"
        cursor.execute(select_query)

        # fill line edits
        for row in cursor:
            self.projectID.setText(str(row[0]))
            self.ngoID.setText(str(row[1]))
            self.projectName.setText(str(row[2]))
            self.scale.setText(str(row[3]))
            self.startDate.setDate(QDate.fromString(str(row[4]), "yyyy-MM-dd"))

        # set projectName to centre of line edit
        self.projectName.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # disable editing of projectID, ngoID, projectName, scale, startDate
        self.projectID.setDisabled(True)
        self.ngoID.setDisabled(True)
        self.projectName.setDisabled(True)
        self.scale.setDisabled(True)
        self.startDate.setDisabled(True)

        # Close the database connection
        connection.close()

    def addWorker(self):
        self.add_worker = WorkerAdd()
        self.add_worker.show()
        self.add_worker.addWorkerDoneBtn.clicked.connect(self.refreshWorkerTable)

    def updateWorker(self):
        workerDetails = []
        for i in range(0, 5):
            workerDetails.append(self.workerDetails.item(self.workerDetails.currentRow(), i).text())

        self.update_worker = WorkerUpdate(workerDetails)
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
            #do the delete procedure of project
            connection = pyodbc.connect(
                    'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
            )
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

class WorkerAdd(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('AddWorker.ui',self)
        self.addWorkerDoneBtn.clicked.connect(self.WorkerAdded)

    def WorkerAdded(self):
        connection = pyodbc.connect(
                'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
        )
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

class WorkerUpdate(QtWidgets.QMainWindow):
    def __init__(self, workerDetails):
        super().__init__()
        uic.loadUi('UpdateWorker.ui',self)
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


def main():
    app = QApplication(sys.argv)
    window = UI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()