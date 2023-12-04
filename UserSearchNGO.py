from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc


class NGODetails(QtWidgets.QMainWindow):  
    def __init__(self):
        super().__init__()

        uic.loadUi('Screens/screen 3.ui', self)  #Screens/UserSignUp.ui

        self.ViewButton.clicked.connect(self.ShowProject)
    
    def ShowProject(self):
        self.ProjectPage = ProjectDetails()
        self.ProjectPage.show()


class ProjectDetails(QtWidgets.QMainWindow):  
    def __init__(self, value):
        self.selectedProject=value
        super().__init__()
        

        uic.loadUi('Screens/screen 4.ui', self)  #Screens/UserSignUp.ui
        self.lineEdit_3.setText(self.selectedProject)
        print(self.selectedProject, "test")
        self.DonateButton.clicked.connect(self.Donate)
    
    def Donate(self):
        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Do You Confirm This Transaction?")
        Dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Yes:
            Dialog2 = QtWidgets.QMessageBox()
            Dialog2.setWindowTitle("Thankyou")
            Dialog2.setText("The Amount Is Successfully Donated. Thankyou")
            Dialog2.exec()
            self.close()
    
            

           



        
class NGOs(QtWidgets.QMainWindow):  
    def __init__(self):
        super().__init__()

        uic.loadUi('Screens/screen2.ui', self)  #Screens/UserSignUp.ui

        self.SelectButton.clicked.connect(self.ShowNGO)
    
    def ShowNGO(self):
        self.NGOPage = NGODetails()
        self.NGOPage.show()
