from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

class NewProject(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Screens/AddProject.ui',self)
        
        # self.setStyleSheet("background-color: lightyellow")
        self.DoneButton.clicked.connect(self.ProjectAdded)
    
    def ProjectAdded(self):
        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Project Is Successfully Added To Yor NGO Data")
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Ok:
            self.close()
