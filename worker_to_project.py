from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

class WorkerToProject(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('Screens/ProjectNewWorker.ui' , self)

        self.DoneButton.clicked.connect(self.NewWorker)

    def NewWorker(self):
        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("The Selected Worker Is Successfully Assigned To The Project")
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Ok:
            self.close()

