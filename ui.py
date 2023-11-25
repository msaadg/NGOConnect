from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys

from user_login import UserLogin
from user_signup import UserSignup
from ngo_login import NGOLogin
from ngo_signup import NGOSignup

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(UI, self).__init__() 
        # Load the .ui file
        uic.loadUi('Screens/HomeScreen.ui', self) 

        self.ngoSignupBtn.clicked.connect(self.NGOSignup)
        self.ngoLoginBtn.clicked.connect(self.NGOLogin)
        self.userSignupBtn.clicked.connect(self.UserSignup)
        self.userLoginBtn.clicked.connect(self.UserLogin)
        self.exitBtn.clicked.connect(self.Exit)

        # self.SearchButton.clicked.connect(self.Search)

    def Exit(self):
        sys.exit()
    
    def UserLogin(self):

        self.userlogin = UserLogin()
        self.userlogin.show()

    def NGOLogin(self):

        self.ngologin = NGOLogin()
        self.ngologin.show()
        self.close()

    def UserSignup(self):

        self.usersignup = UserSignup()
        self.usersignup.show()

    def NGOSignup(self):

        self.ngosignup = NGOSignup()
        self.ngosignup.show()
