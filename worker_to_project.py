from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QSortFilterProxyModel
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
import pyodbc
import connectionString

class WorkerToProject(QtWidgets.QMainWindow):
    def __init__(self, projectID):
        super().__init__()
        uic.loadUi('Screens/ProjectNewWorker.ui', self)

        self.model = QStandardItemModel(self.workers)
        self.proxyModel = QSortFilterProxyModel(self.workers)
        self.proxyModel.setSourceModel(self.model)
        self.workers.setModel(self.proxyModel)

        self.workers.setEditable(True)
        self.workers.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.NoInsert)
        self.workers.completer().setCompletionMode(QtWidgets.QCompleter.CompletionMode.PopupCompletion)
        self.workers.completer().setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        self.workers.lineEdit().textEdited.connect(self.proxyModel.setFilterFixedString)

        self.addWorkerDoneBtn.clicked.connect(lambda: self.assignWorker(projectID))
        self.loadWorkers(projectID)

        # Set the combo box to display empty initially
        self.workers.setCurrentIndex(-1)

    def loadWorkers(self, projectID):
        connection = pyodbc.connect(connectionString.connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT ngoID FROM Project WHERE projectID = ?", projectID)
        ngoID = cursor.fetchall()[0][0]

        # only get those worker who are not currently assigned to the project
        cursor.execute("""
            SELECT w.workerEmail, w.workerName
            FROM Worker w
            WHERE w.workerID NOT IN (
                SELECT wp.workerID
                FROM WorkerProject wp
                WHERE wp.projectID = ?
            ) AND w.ngoID = ?
        """, projectID, ngoID)
        workers = cursor.fetchall()

        for worker in workers:
            item = QStandardItem(worker[0] + " - " + worker[1])
            self.model.appendRow(item)

        connection.close()

    def assignWorker(self, projectID):
        selectedWorker = self.workers.currentText()
        if selectedWorker == "":
            Dialog = QMessageBox()
            Dialog.setWindowTitle("Error")
            Dialog.setText("Please Select A Worker")
            Option = Dialog.exec()
            if Option == QMessageBox.StandardButton.Ok:
                return

        Dialog = QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("The Selected Worker Is Successfully Assigned To The Project")
        Option = Dialog.exec()
        if Option == QMessageBox.StandardButton.Ok:
            selectedWorkerEmail = selectedWorker.split(' - ')[0]

            connection = pyodbc.connect(connectionString.connection_string)
            
            cursor = connection.cursor()
            cursor.execute("SELECT workerID FROM Worker WHERE workerEmail = ?", selectedWorkerEmail)
            workerID = cursor.fetchall()[0][0]
            cursor.execute("INSERT INTO WorkerProject VALUES (?, ?, ?)", workerID, projectID, "Assigned")
            connection.commit()
            connection.close()
            self.close()
