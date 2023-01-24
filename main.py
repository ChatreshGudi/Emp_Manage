# import PyQt6
from PyQt6.uic import loadUi
from PyQt6 import *
from PyQt6.QtWidgets import QStackedWidget, QApplication, QMainWindow, QWidget, QFileDialog, QLineEdit
import sys
import os
from emplib import *

class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        loadUi("UI_Files/Main.ui", self)
        
        # Widgets

        ## Home Page
        self.opendb_btn.clicked.connect(self.openDB) # Opening A Employee DB file.
        self.newdb_btn.clicked.connect(self.newDB) # Creating a new Employee DB file.
        
        ## Login Page
        self.rand_pass_btn.clicked.connect(self.rand_pass) # Generating a random password.
        self.login_btn.clicked.connect(self.login) # Login

    # Home Page

    def openDB(self):
        filepath = QFileDialog.getOpenFileName(self, "Open Employee Database", "c:\\", "EMP DB Files (*.json);;") # Opening a file.
        self.emp_man = EmployeeManagement(filepath[0]) # Creating an employee managment system object.
        self.stackedWidget.setCurrentWidget(self.Login_Page) # Opening the login Page.

    def newDB(self):
        filepath = QFileDialog.getSaveFileName(self, "Open Employee Database", "c:\\", "EMP DB Files (*.json);;")
        self.emp_man = EmployeeManagement(filepath[0]) # Creating an employee managment system object.
        self.stackedWidget.setCurrentWidget(self.Login_Page) # Opening the login Page.

    # Login Page

    def rand_pass(self):
        self.pass_text.setText(random_pas_gen())
    
    def login(self):
        name = self.name_text.text()
        passw = self.pass_text.text()
        if self.Emp.isChecked():
            type = "Employee"
        elif self.Admin.isChecked():
            type = "Admin"
        else:
            self.error_msg.setText("Please select a user type.")
        if type:
            if self.emp_man.verify_login(type, name, passw):
                if type == "Admin":
                    self.stackedWidget.setCurrentWidget(self.Main_Page)
                elif type == "Employee":
                    pass
app = QApplication([])
win = Window()
win.show()
app.exec()