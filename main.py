from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(UI, self).__init__() 
        # Load the .ui file
        uic.loadUi('HomeScreen.ui', self) 
        # self.setStyleSheet("background-color: lightyellow")

        self.NGOSignUpButton.clicked.connect(self.NGOSignUp)
        self.NGOLoginButton.clicked.connect(self.NGOLogin)
        self.UserSignUpButton.clicked.connect(self.UserSignUp)
        self.UserLoginButton.clicked.connect(self.UserLogin)
        self.ExitButton.clicked.connect(self.Exit)

        # self.SearchButton.clicked.connect(self.Search)

    def Exit(self):
        sys.exit()
    
    def UserLogin(self):

        self.view_userlogin = ViewUserLogin()
        self.view_userlogin.show()

    def NGOLogin(self):

        self.view_ngologin = ViewNgoLogin()
        self.view_ngologin.show()

    def UserSignUp(self):

        self.view_usersignup = ViewUserSignUp()
        self.view_usersignup.show()

    def NGOSignUp(self):

        self.view_ngosignup = ViewNgoSignUp()
        self.view_ngosignup.show()

class ViewNgoSignUp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('NGOSignUp.ui' , self)
        # self.setStyleSheet("background-color: yellow")
        self.CreateNGOButton.clicked.connect(self.NGOCreate)

        # set Password and Confirm Password to hidden
        self.ngoSignUpPass.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.ngoSignUpConfirmPass.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def NGOCreate(self):
        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Your NGO Is Successfully Added To The Database")
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Ok:
            self.close()

        #Dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)



class ViewUserLogin(QtWidgets.QMainWindow):  
    def __init__(self):
        super().__init__()

        uic.loadUi('UserLogin.ui', self)
        # self.setStyleSheet("background-color: yellow")


class ViewUserSignUp(QtWidgets.QMainWindow):  
    def __init__(self):
        super().__init__()

        uic.loadUi('UserSignUp.ui', self)
        # self.setStyleSheet("background-color: yellow")
        self.CreateUserButton.clicked.connect(self.UserCreate)

    def UserCreate(self):
        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("You Are Successfully Registered")
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Ok:
            self.close()


class ViewNgoLogin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('NGOLogin.ui' , self)
        # self.setStyleSheet("background-color: yellow")

        # set NGO Password to be hidden
        self.ngoPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.NGOEnterButton.clicked.connect(self.ShowNGO)

    def ShowNGO(self):
        self.view_ngopage = ViewNgoPage()
        self.view_ngopage.show()
        self.close()

    
class ViewNgoPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('NGOPage.ui' , self)
        
        # self.setStyleSheet("background-color: lightyellow")
        self.ProjectViewButton.clicked.connect(self.ShowProject)
        self.NewProjectButton.clicked.connect(self.AddProject)
        self.DeleteButton.clicked.connect(self.DeleteProject)
    
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


class NewProject(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('AddProject.ui',self)
        
        # self.setStyleSheet("background-color: lightyellow")
        self.DoneButton.clicked.connect(self.ProjectAdded)
    
    def ProjectAdded(self):
        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Project Is Successfully Added To Yor NGO Data")
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Ok:
            self.close()



class ViewProject(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super().__init__()

        # Load the .ui file
        uic.loadUi('ViewProject.ui', self)

        self.loadProjectData()
        self.refreshWorkerTable()
        self.addWorkerBtn.clicked.connect(self.addWorker)
        self.removeWorkerBtn.clicked.connect(self.removeWorker)
        self.updateBtn.clicked.connect(self.updateWorker)

        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.refreshWorkerTable)
        # self.timer.start(5000)

    def refreshWorkerTable(self):
        self.workerDetails.clearContents()
        self.workerDetails.setRowCount(0)
        self.populateWorkerTable()


    def populateWorkerTable(self):
        # connection = pyodbc.connect(
        #         'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
        # )

        server = 'SABIR\SQLEXPRESS'
        database = 'NGOConnect'  # Name of your NGOConnect database
        use_windows_authentication = True 
        connection = pyodbc.connect(
                f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
        )

        cursor = connection.cursor()

        # TODO: Write SQL query to fetch Workers Data
        select_query = "SELECT workerID, workerEmail, workerName, gender, age from Worker where workerID in (select workerID from WorkerProject where projectID = 1)"
        cursor.execute(select_query)

        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.workerDetails.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.workerDetails.setItem(row_index, col_index, item)

        # Close the database connection
        connection.close()

        # Adjust content display
        header = self.workerDetails.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

    def loadProjectData(self):
        self.setWindowTitle("Project")

        # connection = pyodbc.connect(
        #         'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
        # )

        server = 'SABIR\SQLEXPRESS'
        database = 'NGOConnect'  # Name of your NGOConnect database
        use_windows_authentication = True 
        connection = pyodbc.connect(
                f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
        )

        cursor = connection.cursor()

        select_query = "SELECT projectID, name, projectName, scale, startDate from Project p, NGO n where p.ngoID = n.ngoID and projectID = 1"
        cursor.execute(select_query)

        # fill line edits
        for row in cursor:
            self.projectID.setText(str(row[0]))
            self.ngoName.setText(str(row[1]))
            self.projectName.setText(str(row[2]))
            self.scale.setText(str(row[3]))
            self.startDate.setDate(QDate.fromString(str(row[4]), "yyyy-MM-dd"))

        # set projectName to centre of line edit
        self.projectName.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # disable editing of projectID, ngoID, projectName, scale, startDate
        self.projectID.setDisabled(True)
        self.ngoName.setDisabled(True)
        self.projectName.setDisabled(True)
        self.scale.setDisabled(True)
        self.startDate.setDisabled(True)

        # Close the database connection
        connection.close()

    def addWorker(self):
        self.add_worker = WorkerAdd()
        self.add_worker.show()
        self.add_worker.addWorkerDoneBtn.clicked.connect(self.refreshWorkerTable)

    def updateWorker(self):
        workerDetails = []
        for i in range(0, 5):
            workerDetails.append(self.workerDetails.item(self.workerDetails.currentRow(), i).text())

        self.update_worker = WorkerUpdate(workerDetails)
        self.update_worker.show()
        self.update_worker.updateWorkerDoneBtn.clicked.connect(self.refreshWorkerTable)

    def removeWorker(self):
        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Are You Sure You Want To Remove This Worker?")
        Dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        Option = Dialog.exec()
        x = 0
        if Option == QtWidgets.QMessageBox.StandardButton.Yes:
            #do the delete procedure of project
            # connection = pyodbc.connect(
            #         'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
            # )
            server = 'SABIR\SQLEXPRESS'
            database = 'NGOConnect'  # Name of your NGOConnect database
            use_windows_authentication = True 
            connection = pyodbc.connect(
                    f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
            )
            cursor = connection.cursor()

            delete_query1 = """
                DELETE FROM WorkerProject
                WHERE workerID = ? and projectID = ?
            """

            delete_query2 = """
                DELETE FROM Worker
                WHERE workerID = ? and ngoID = ?
            """

            cursor.execute(delete_query1, (int(self.workerDetails.item(self.workerDetails.currentRow(), 0).text()), 1))
            cursor.execute(delete_query2, (int(self.workerDetails.item(self.workerDetails.currentRow(), 0).text()), 1))
            
            connection.commit()
            connection.close()
            self.refreshWorkerTable()

class WorkerAdd(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('AddWorker.ui',self)
        self.addWorkerDoneBtn.clicked.connect(self.WorkerAdded)

    def WorkerAdded(self):
        # connection = pyodbc.connect(
        # )
        server = 'SABIR\SQLEXPRESS'
        database = 'NGOConnect'  # Name of your NGOConnect database
        use_windows_authentication = True 
        connection = pyodbc.connect(
                f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
        )
        cursor = connection.cursor()

        insert_query1 = """
            INSERT INTO Worker
            ([ngoID], [workerEmail], [workerName], [workerPassword], [gender], [age])
            VALUES (?, ?, ?, ?, ?, ?)
        """

        insert_query2 = """
            INSERT INTO WorkerProject
            ([workerID], [projectID], [workerStatus])
            VALUES (?, ?, ?)
        """

        cursor.execute(insert_query1, (1, self.workerEmail.text(), self.workerName.text(), self.workerPassword.text(), 
                                      self.gender.text(), int(self.age.text())))
        
        cursor.execute(insert_query2, (cursor.execute("SELECT IDENT_CURRENT('Worker')").fetchone()[0], 1, "Active"))
        
        connection.commit()
        connection.close()


        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Worker Is Successfully Added")
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Ok:
            self.close()

class WorkerUpdate(QtWidgets.QMainWindow):
    def __init__(self, workerDetails):
        super().__init__()
        uic.loadUi('UpdateWorker.ui',self)
        #set window title
        self.setWindowTitle("Update Worker")
        self.workerEmail.setText(workerDetails[1])
        self.workerName.setText(workerDetails[2])
        self.gender.setText(workerDetails[3])
        self.age.setText(workerDetails[4])

        self.updateWorkerDoneBtn.clicked.connect(lambda: self.WorkerUpdated(workerDetails))

    def WorkerUpdated(self, workerDetails):
        # connection = pyodbc.connect(
        #         'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
        # )
        server = 'SABIR\SQLEXPRESS'
        database = 'NGOConnect'  # Name of your NGOConnect database
        use_windows_authentication = True 
        connection = pyodbc.connect(
                f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
        )

        cursor = connection.cursor()

        update_query = """
            UPDATE Worker
            SET workerEmail = ?, workerName = ?, gender = ?, age = ?
            WHERE workerID = ?
        """

        cursor.execute(update_query, (
            self.workerEmail.text(),
            self.workerName.text(),
            self.gender.text(),
            int(self.age.text()),
            workerDetails[0]  # This is the workerID from the workerDetails list
        ))
        
        connection.commit()
        connection.close()

        Dialog = QtWidgets.QMessageBox()
        Dialog.setWindowTitle("Confirmation Box")
        Dialog.setText("Worker Details Successfully Updated")
        Option = Dialog.exec()
        if Option == QtWidgets.QMessageBox.StandardButton.Ok:
            self.close()


def main():
    app = QApplication(sys.argv)
    window = UI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()