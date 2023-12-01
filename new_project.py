from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

class NewProject(QtWidgets.QMainWindow):
    def __init__(self, ngoID):
        super().__init__()
        uic.loadUi('Screens/AddProject.ui',self)
        
        self.projectStartDate.setDate(QDate.currentDate())

        self.projectDoneBtn.clicked.connect(lambda: self.ProjectAdded(ngoID))
        self.projectCancelBtn.clicked.connect(lambda: self.close())
    
    def ProjectAdded(self, ngoID):
        # get projectName, prjectScale, projectStartDate, projectEndDate
        projectName = self.projectName.text()
        projectScale = self.projectScale.text()
        projectStartDate = self.projectStartDate.date()

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
        cursor.execute("SELECT projectName FROM Project")
        projectNames = [x[0] for x in cursor.fetchall()]
        
        if projectScale.isdigit() == False:
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Project Scale Must Be An Integer")
            Dialog.exec()
            return
        
        if projectName in projectNames:
            Dialog = QtWidgets.QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Project Name Already Exists \n Please Enter A Different Project Name")
            Dialog.exec()
            return

        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Project Is Successfully Added To Yor NGO Data")
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Ok:
            cursor.execute("INSERT INTO Project(ngoID, projectName, scale, startDate) VALUES(?, ?, ?, ?)", ngoID, projectName, projectScale, projectStartDate.toString("yyyy-MM-dd"))
            connection.commit()
            connection.close()

            self.close()