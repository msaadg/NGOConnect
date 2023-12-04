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

        #disable from and to date
        self.fromDateEdit.setEnabled(False)
        self.toDateEdit.setEnabled(False)

        # if fromCheckbox is checked enable fromDateEdit
        self.fromCheckbox.stateChanged.connect(lambda: self.fromDateEdit.setEnabled(self.fromCheckbox.isChecked()))
        # if toCheckbox is checked enable toDateEdit
        self.toCheckbox.stateChanged.connect(lambda: self.toDateEdit.setEnabled(self.toCheckbox.isChecked()))

        self.addWorkerBtn.clicked.connect(lambda: self.AddWorker(ngoID))
        self.removeWorkerBtn.clicked.connect(lambda: self.removeWorker(ngoID))
        self.updateWorkerBtn.clicked.connect(lambda: self.UpdateWorker(ngoID))
        self.searchWorkerBtn.clicked.connect(lambda: self.searchWorker(ngoID))

        self.loadSearchData(ngoID)
        self.loadWorkersData(ngoID)

    def refreshData(self, ngoID):
        self.loadWorkersData(ngoID)

    def loadSearchData(self, ngoID):
        # connection = pyodbc.connect(
        #         'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
        # )

        server = 'SABIR\SQLEXPRESS'
        database = 'NGOConnect'  # Name of your NGOConnect database
        use_windows_authentication = True 
        connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')

        cursor = connection.cursor()
        #load all workers email in emailCombobox
        cursor.execute("SELECT workerEmail FROM Worker WHERE ngoID = ?", ngoID)
        self.emailCombobox.clear()
        self.emailCombobox.addItem("")
        for row in cursor.fetchall():
            self.emailCombobox.addItem(row[0])

        #load all workers name in nameCombobox
        cursor.execute("SELECT workerName FROM Worker WHERE ngoID = ?", ngoID)
        self.nameCombobox.clear()
        self.nameCombobox.addItem("")
        for row in cursor.fetchall():
            self.nameCombobox.addItem(row[0])

        connection.close()

    def loadWorkersData(self, ngoID):
        # connection = pyodbc.connect(
        #         'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
        # )

        server = 'SABIR\SQLEXPRESS'
        database = 'NGOConnect'  # Name of your NGOConnect database
        use_windows_authentication = True 
        connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')

        cursor = connection.cursor()

        header = self.workerDetails.horizontalHeader()
        for i in range(5):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        self.workerDetails.clearContents()
        self.workerDetails.setRowCount(0)

        cursor.execute("SELECT workerEmail, workerName, gender, age, dateAdded FROM Worker WHERE ngoID = ?", ngoID)
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.workerDetails.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.workerDetails.setItem(row_index, col_index, item)
                self.workerDetails.item(row_index, col_index).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        connection.close()


    def searchWorker(self, ngoID):
        self.loadWorkersData(ngoID)

        # Get the selected email
        selected_email = self.emailCombobox.currentText()

        if selected_email and selected_email != "":  # Assuming "" or some default value for no selection
            for row in range(self.workerDetails.rowCount() - 1, -1, -1):
                if self.workerDetails.item(row, 0).text() != selected_email:
                    self.workerDetails.removeRow(row)

        # Get the selected name
        selected_name = self.nameCombobox.currentText()

        if selected_name and selected_name != "":  # Assuming "" or some default value for no selection
            for row in range(self.workerDetails.rowCount() - 1, -1, -1):
                if self.workerDetails.item(row, 1).text() != selected_name:
                    self.workerDetails.removeRow(row)

        # Get the selected gender
        selected_gender = self.genderCombobox.currentText()

        if selected_gender and selected_gender != "":  # Assuming "" or some default value for no selection
            for row in range(self.workerDetails.rowCount() - 1, -1, -1):
                if self.workerDetails.item(row, 2).text() != selected_gender:
                    self.workerDetails.removeRow(row)

        # Get the selected age
        selected_age = self.ageCombobox.currentText()
        # < 20
        # < 30
        # < 40
        # < 50

        if selected_age and selected_age != "":  # Assuming "" or some default value for no selection
            for row in range(self.workerDetails.rowCount() - 1, -1, -1):
                if selected_age == "< 50":
                    if int(self.workerDetails.item(row, 3).text()) >= 50:
                        self.workerDetails.removeRow(row)
                elif selected_age == "< 40":
                    if int(self.workerDetails.item(row, 3).text()) >= 40:
                        self.workerDetails.removeRow(row)
                elif selected_age == "< 30":
                    if int(self.workerDetails.item(row, 3).text()) >= 30:
                        self.workerDetails.removeRow(row)
                elif selected_age == "< 20":
                    if int(self.workerDetails.item(row, 3).text()) >= 20:
                        self.workerDetails.removeRow(row)

        #handle all errors
        if self.fromCheckbox.isChecked():
            selected_from_date = self.fromDateEdit.date().toString("yyyy-MM-dd")
        else:
            selected_from_date = ""

        if self.toCheckbox.isChecked():
            selected_to_date = self.toDateEdit.date().toString("yyyy-MM-dd")
        else:
            selected_to_date = ""
            
        if selected_from_date != "" and selected_to_date != "":
            if selected_from_date > selected_to_date:
                Dialog = QtWidgets.QMessageBox()
                Dialog.setWindowTitle("Error")
                Dialog.setText("From Date Must Be Less Than To Date")
                Dialog.exec()
                return

            elif selected_to_date < selected_from_date:
                Dialog = QtWidgets.QMessageBox()
                Dialog.setWindowTitle("Error")
                Dialog.setText("To Date Must Be Greater Than From Date")
                Dialog.exec()
                return
            
            elif selected_from_date <= "2000-01-01":
                Dialog = QtWidgets.QMessageBox()
                Dialog.setWindowTitle("Error")
                Dialog.setText("From Date Must Be Greater Than 2000-01-01")
                Dialog.exec()
                return
            
            elif selected_to_date >= QDate.currentDate().toString("yyyy-MM-dd"):
                Dialog = QtWidgets.QMessageBox()
                Dialog.setWindowTitle("Error")
                Dialog.setText("To Date Must Be Less Than Current Date")
                Dialog.exec()
                return
            
            for row in range(self.workerDetails.rowCount() - 1, -1, -1):
                if self.workerDetails.item(row, 4).text() < selected_from_date or self.workerDetails.item(row, 4).text() > selected_to_date:
                    self.workerDetails.removeRow(row)
        
        elif selected_from_date != "" and selected_to_date == "":
            if selected_from_date >= QDate.currentDate().toString("yyyy-MM-dd"):
                Dialog = QtWidgets.QMessageBox()
                Dialog.setWindowTitle("Error")
                Dialog.setText("From Date Must Be Less Than Current Date")
                Dialog.exec()
                return
            
            elif selected_from_date <= "2000-01-01":
                Dialog = QtWidgets.QMessageBox()
                Dialog.setWindowTitle("Error")
                Dialog.setText("From Date Must Be Greater Than 2000-01-01")
                Dialog.exec()
                return
            
            for row in range(self.workerDetails.rowCount() - 1, -1, -1):
                if self.workerDetails.item(row, 4).text() < selected_from_date:
                    self.workerDetails.removeRow(row)
            
        elif selected_from_date == "" and selected_to_date != "":
            if selected_to_date >= QDate.currentDate().toString("yyyy-MM-dd"):
                Dialog = QtWidgets.QMessageBox()
                Dialog.setWindowTitle("Error")
                Dialog.setText("To Date Must Be Less Than Current Date")
                Dialog.exec()
                return
            
            elif selected_to_date <= "2000-01-01":
                Dialog = QtWidgets.QMessageBox()
                Dialog.setWindowTitle("Error")
                Dialog.setText("To Date Must Be Greater Than 2000-01-01")
                Dialog.exec()
                return

            for row in range(self.workerDetails.rowCount() - 1, -1, -1):
                if self.workerDetails.item(row, 4).text() > selected_to_date:
                    self.workerDetails.removeRow(row)
                

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