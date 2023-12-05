from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc



class NGODetails(QtWidgets.QMainWindow):  
    def __init__(self, _selected_NGO, _userID):
        self.selected_NGO=_selected_NGO
        self.userID=_userID
        self.view_button_connection = None
        self.change=pyqtSignal(int)
        
        super().__init__()

        uic.loadUi('Screens/screen 3.ui', self)  #Screens/UserSignUp.ui
        
        
        
        
        self.lineEdit.setText(self.selected_NGO)
        self.lineEdit.setEnabled(False)
        server = 'SABIR\SQLEXPRESS'
        database = 'NGOConnect'  # Name of your NGOConnect database
        connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')
        cursor = connection.cursor()
        cursor.execute("select address from NGO where name=?", self.selected_NGO)
        ngo_address=cursor.fetchall()[0][0]
        cursor.execute("select ngoEmail from NGO where name=?", self.selected_NGO)
        ngo_email=cursor.fetchall()[0][0]
        self.lineEdit_2.setText(ngo_address)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_3.setText(ngo_email)
        self.lineEdit_3.setEnabled(False)
        cursor.execute("select ngoID from NGO where name=?", self.selected_NGO)
        ngo_ID=cursor.fetchall()[0][0]
        cursor.execute("""select projectName, categoryName, areaName
                       from Project where ngoID=?
                       """, ngo_ID)
        data=cursor.fetchall()
        rows=len(data)
        cols=len(data[0])
        
        self.tableWidget.setRowCount(rows)
        self.tableWidget.setColumnCount(cols)
        for row_index, row_data in enumerate(data):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.tableWidget.setItem(row_index, col_index, item)
        # self.tableWidget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        connection.close()

        self.tableWidget.itemSelectionChanged.connect(lambda: self.handle_selection_changed(self.selected_NGO, self.userID, data, ngo_ID))
    def handle_selection_changed(self, selected_NGO, userID, data, ngo_ID):
        selected_items = self.tableWidget.selectedItems()
        if selected_items:
            selected_row = selected_items[0].row()
            selected_project = data[selected_row][0]
            selected_category = data[selected_row][1]
            selected_area = data[selected_row][2]
            if self.view_button_connection:
                self.ViewButton.clicked.disconnect()
            self.ViewButton.clicked.connect(lambda: self.ShowProject(selected_project, selected_NGO, ngo_ID, userID, selected_category, selected_area))
            self.view_button_connection = True

    def ShowProject(self, selected_project, selected_NGO, ngo_ID, userID, selected_category, selected_area):
        server = 'SABIR\SQLEXPRESS'
        database = 'NGOConnect'  # Name of your NGOConnect database
        connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')
        cursor = connection.cursor()
        cursor.execute("select projectID from Project where projectName=? and areaName=? and categoryName=?", selected_project, selected_area, selected_category)
        projectID=cursor.fetchall()[0][0]
        cursor.execute("select getdate()")
        donationDateTime=cursor.fetchall()[0][0]

        self.ProjectPage = ProjectDetails(projectID, selected_NGO, ngo_ID, userID, donationDateTime)
        self.ProjectPage.show()
        # self.ProjectPage.DonateButton.clicked.connect(lambda: self.ProjectPage.Donate(projectID, ngo_ID, userID, donationDateTime))
        # self.ProjectPage.DonateButton.clicked.connect(self._donateButton)


    # def _donateButton(self):
    #     self.donateButton=1
    #     self.change.emit()

class ProjectDetails(QtWidgets.QMainWindow):  
    
    def __init__(self, _projectID, _ngo_Name, _ngo_ID, _userID, _donationDateTime):
        self.ngo_Name=_ngo_Name
        self.ngo_ID=_ngo_ID
        self.userID=_userID
        self.donationDateTime=_donationDateTime
        self.projectID=_projectID
        
        # self.Dialog = QtWidgets.QMessageBox()
        super().__init__()
        

        uic.loadUi('Screens/screen 4.ui', self)  #Screens/UserSignUp.ui
        self.lineEdit_3.setText(self.ngo_Name)
        self.lineEdit_3.setEnabled(False)
        self.DonateButton.clicked.connect(lambda: self.Donate(self.projectID, self.ngo_ID, self.userID, _donationDateTime))
    
    def Donate(self, _project_ID, _ngo_ID, _userID, _donationDateTime):
        _Amount=int(self.lineEdit.text())
        # print(_project_ID, _ngo_ID, _userID, _donationDateTime, _Amount)
        self.Dialog = QtWidgets.QMessageBox()
        self.Dialog.setWindowTitle("Confirmation Box")
        self.Dialog.setText("Do You Confirm This Transaction?")
        self.Dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        Option = self.Dialog.exec()

        if Option == QtWidgets.QMessageBox.StandardButton.Yes:
            Dialog2 = QtWidgets.QMessageBox()
            Dialog2.setWindowTitle("Thankyou")
            Dialog2.setText("The Amount Is Successfully Donated. Thankyou")
            Dialog2.exec()
            self.close()
            server = 'SABIR\SQLEXPRESS'
            database = 'NGOConnect'  # Name of your NGOConnect datab
            connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')
            cursor = connection.cursor()
            add_query="""
                INSERT INTO Donation(projectID, userID, donationDateTime, amount)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(add_query, _project_ID, _userID, _donationDateTime, _Amount)

            connection.commit()
            connection.close()


    
            

           



        
class NGOs(QtWidgets.QMainWindow):  
    def __init__(self, _selected_Category, _selected_Area,):
        self.selected_Category=_selected_Category
        self.selected_Area=_selected_Area
        super().__init__()
        uic.loadUi('Screens/screen2.ui', self)  #Screens/UserSignUp.ui
        server = 'SABIR\SQLEXPRESS'
        database = 'NGOConnect' 
        connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;')
        cursor=connection.cursor()
        if self.selected_Area!=None and self.selected_Category!=None:
            cursor.execute("""
                            select projectName from Project
                           where categoryName=? and areaName=?
                            """, self.selected_Category, self.selected_Area)
        elif self.selected_Area!=None:
            cursor.execute("""
                            select projectName from Project
                           where areaName=?
                            """, self.selected_Area)
        elif self.selected_Category!=None:
            cursor.execute("""
                            select projectName from Project
                           where categoryName=?
                            """, self.selected_Category)


        data=cursor.fetchall()
        # rows=len(data)
        # self.tableWidget.setRowCount(rows)
        for i in data:
            print(data)


        self.SelectButton.clicked.connect(self.ShowNGO)
    
    def ShowNGO(self):
        self.NGOPage = NGODetails()
        self.NGOPage.show()
