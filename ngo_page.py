from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

from worker_data import WorkerData
from view_project import ViewProject
from new_project import NewProject

class NGOPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Screens/NGOPage.ui' , self)
        
        # self.setStyleSheet("background-color: lightyellow")
        self.ProjectViewButton.clicked.connect(self.ShowProject)
        self.NewProjectButton.clicked.connect(self.AddProject)
        self.DeleteButton.clicked.connect(self.DeleteProject)
        self.WorkerButton.clicked.connect(self.Worker)

    def Worker(self):
        self.view_project = WorkerData()
        self.view_project.show()
    
       
    def DeleteProject(self):
        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Are You Sure You Want To Delete This Project?")
        Dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Yes:
            #do the delete procedure of project
            print("abc")
    

        #Dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

    def ShowProject(self):
        self.view_project = ViewProject()
        self.view_project.show()
    
    def AddProject(self):
        self.new_project = NewProject()
        self.new_project.show()
