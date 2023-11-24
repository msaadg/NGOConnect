from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

from add_worker import AddWorker
from update_worker import UpdateWorker

class WorkerData(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Screens/WorkerPage.ui' , self)

        self.AddWorkerButton.clicked.connect(self.AddWorker)
        self.UpdateWorkerButton.clicked.connect(self.UpdateWorker)
        self.DeleteWorkerButton.clicked.connect(self.removeWorker)

    def AddWorker(self):
        self.new_worker = AddWorker()
        self.new_worker.show()


    def UpdateWorker(self):
        self.worker_update = UpdateWorker()
        self.worker_update.show()

    def removeWorker(self):
        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Are You Sure You Want To Remove This Worker?")
        Dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        Option = Dialog.exec()

