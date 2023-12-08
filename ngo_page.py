from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

from worker_data import WorkerData
from view_project import ViewProject
from new_project import NewProject
from new_area import NewArea
from new_category import NewCategory
import connectionString

class NGOPage(QtWidgets.QMainWindow):
    def __init__(self, ngoID):
        super().__init__()
        uic.loadUi('Screens/NGOPage.ui' , self)
        #set windows title
        self.setWindowTitle("NGO Screen")

        self.ngoName.setDisabled(True)
        self.ngoEmail.setDisabled(True)
        self.ngoAddress.setDisabled(True)
        self.ngoRegDate.setDisabled(True)
        self.ngoSaveBtn.setDisabled(True)

        
        self.ngoEditBtn.clicked.connect(self.EditNGO)
        self.ngoSaveBtn.clicked.connect(lambda: self.SaveNGO(ngoID))

        self.ngoWorkersBtn.clicked.connect(lambda: self.Workers(ngoID))

        self.ngoAddAreaBtn.clicked.connect(lambda: self.AddArea(ngoID))
        self.ngoDeleteAreaBtn.clicked.connect(lambda: self.DeleteArea(ngoID))

        self.ngoAddCategoryBtn.clicked.connect(lambda: self.AddCategory(ngoID))
        self.ngoDeleteCategoryBtn.clicked.connect(lambda: self.DeleteCategory(ngoID))

        self.ngoViewProjectBtn.clicked.connect(self.ShowProject)
        self.ngoAddProjectBtn.clicked.connect(lambda: self.AddProject(ngoID))
        self.ngoDeleteProjectBtn.clicked.connect(lambda: self.DeleteProject(ngoID))

        self.ngoLogoutBtn.clicked.connect(self.Logout)

        self.loadData(ngoID)

    def refreshData(self, ngoID):
        self.loadData(ngoID)

    def loadData(self, ngoID):
        connection = pyodbc.connect(connectionString.connection_string)
        cursor=connection.cursor()
        cursor.execute("SELECT name, ngoEmail, address, regDate FROM NGO WHERE ngoID = ?", ngoID)
        ngoData = cursor.fetchall()[0]
        self.ngoName.setText(ngoData[0])
        self.ngoEmail.setText(ngoData[1])
        self.ngoAddress.setText(ngoData[2])
        self.ngoRegDate.setDate(ngoData[3])

        self.ngoName.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ngoEmail.home(False)
        self.ngoAddress.home(False)


        cursor.execute("SELECT areaName FROM Area WHERE areaCode in (SELECT areaCode FROM OperatingAreas WHERE ngoID = ?)", ngoID)
        areas = [x[0] for x in cursor.fetchall()]
        model = QtCore.QStringListModel()
        model.setStringList(areas)
        self.ngoOperatingAreas.setModel(model)


        cursor.execute("SELECT categoryName FROM Category WHERE categoryName in (SELECT categoryName FROM OperatingCategories WHERE ngoID = ?)", ngoID)
        categories = [x[0] for x in cursor.fetchall()]
        model = QtCore.QStringListModel()
        model.setStringList(categories)
        self.ngoOperatingCategories.setModel(model)

        header = self.ngoProjects.horizontalHeader()
        for i in range(self.ngoProjects.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        self.ngoProjects.clearContents()
        self.ngoProjects.setRowCount(0)

        cursor.execute("SELECT projectName, scale, startDate, endDate FROM Project WHERE ngoID = ?", ngoID)
        for row_number, row_data in enumerate(cursor):
            self.ngoProjects.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if column_number == 3 and data == None:
                    data = "-"
                self.ngoProjects.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                self.ngoProjects.item(row_number, column_number).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        # Close the database connection
        connection.close()

    def EditNGO(self):
        self.ngoName.setDisabled(False)
        self.ngoEmail.setDisabled(False)
        self.ngoAddress.setDisabled(False)
        self.ngoRegDate.setDisabled(False)

        self.ngoSaveBtn.setDisabled(False)

        #change edit button to cancel button
        self.ngoEditBtn.setText("Cancel")
        self.ngoEditBtn.clicked.connect(self.CancelEdit)

    def CancelEdit(self):
        self.ngoName.setDisabled(True)
        self.ngoEmail.setDisabled(True)
        self.ngoAddress.setDisabled(True)
        self.ngoRegDate.setDisabled(True)

        self.ngoSaveBtn.setDisabled(True)

        self.ngoEditBtn.setText("Edit")
        self.ngoEditBtn.clicked.connect(self.EditNGO)


    def SaveNGO(self, ngoID):
        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Are You Sure You Want To Save The Changes?")
        Dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Yes:
            connecion = pyodbc.connect(connectionString.connection_string)
            cursor = connecion.cursor()
            cursor.execute("UPDATE NGO SET name = ?, ngoEmail = ?, address = ?, regDate = ? WHERE ngoID = ?", self.ngoName.text(), self.ngoEmail.text(), self.ngoAddress.text(), self.ngoRegDate.date().toPyDate(), ngoID)
            print("updated")
            print(ngoID)
            connecion.commit()
            connecion.close()

            self.ngoName.setDisabled(True)
            self.ngoEmail.setDisabled(True)
            self.ngoAddress.setDisabled(True)
            self.ngoRegDate.setDisabled(True)
            self.ngoSaveBtn.setDisabled(True)

            #change text from cancel to edit
            self.ngoEditBtn.setText("Edit")
            self.ngoEditBtn.setDisabled(False)

    def Workers(self, ngoID):
        self.workers_page = WorkerData(ngoID)
        self.workers_page.show()

    def AddArea(self, ngoID):
        self.new_area = NewArea(ngoID)
        self.new_area.show()
        self.new_area.areaDoneBtn.clicked.connect(lambda: self.refreshData(ngoID))

    def DeleteArea(self, ngoID):
        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Are You Sure You Want To Delete This Area?")
        Dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Yes:
            #get selected row from QListView
            indexes = self.ngoOperatingAreas.selectionModel().selectedIndexes()
            if indexes:
                selected_index = indexes[0]  # Assuming single selection
                areaName = selected_index.data()

            connection = pyodbc.connect(connectionString.connection_string)
            cursor = connection.cursor()

            cursor.execute("SELECT areaCode FROM Area WHERE areaName = ?", areaName)
            areaCode = cursor.fetchall()[0][0]
            cursor.execute("DELETE FROM OperatingAreas WHERE areaCode = ?", areaCode)

            connection.commit()
            connection.close()
            self.refreshData(ngoID)

    def AddCategory(self, ngoID):
        self.new_category = NewCategory(ngoID)
        self.new_category.show()
        self.new_category.categoryDoneBtn.clicked.connect(lambda: self.refreshData(ngoID))

    def DeleteCategory(self, ngoID):
        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Are You Sure You Want To Delete This Category?")
        Dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Yes:
            indexes = self.ngoOperatingCategories.selectionModel().selectedIndexes()
            if indexes:
                selected_index = indexes[0]  # Assuming single selection
                categoryName = selected_index.data()


            connection = pyodbc.connect(connectionString.connection_string)
            cursor = connection.cursor()

            cursor.execute("DELETE FROM OperatingCategories WHERE categoryName = ?", categoryName)

            connection.commit()
            connection.close()
            self.refreshData(ngoID)


    def ShowProject(self):
        projectName = self.ngoProjects.item(self.ngoProjects.currentRow(), 0).text()
        
        connection = pyodbc.connect(connectionString.connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT projectID FROM Project WHERE projectName = ?", projectName)
        projectID = cursor.fetchall()[0][0]

        self.projects_page = ViewProject(projectID)
        self.projects_page.show()

    def AddProject(self, ngoID):
        self.new_project = NewProject(ngoID)
        self.new_project.show()
        self.new_project.projectDoneBtn.clicked.connect(lambda: self.refreshData(ngoID))
       
    def DeleteProject(self, ngoID):
        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Are You Sure You Want To Delete This Project?")
        Dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Yes:
            projectName = self.ngoProjects.item(self.ngoProjects.currentRow(), 0).text()
            connection = pyodbc.connect(connectionString.connection_string)
            cursor = connection.cursor()

            cursor.execute("SELECT projectID FROM Project WHERE projectName = ?", projectName)
            projectID = cursor.fetchall()[0][0]

            #delete from WorkerProject
            cursor.execute("DELETE FROM WorkerProject WHERE projectID = ?", projectID)

            #delete from Donations
            cursor.execute("DELETE FROM Donation WHERE projectID = ?", projectID)

            #delete from project
            cursor.execute("DELETE FROM Project WHERE projectName = ?", projectName)


            connection.commit()
            connection.close()
            self.refreshData(ngoID)

    def Logout(self):
        self.close()
        #open homescreen
        from ui import UI
        self.home = UI()
        self.home.show()
        