# import PyQt6
from PyQt6.uic import loadUi
from PyQt6 import *
from PyQt6.QtWidgets import QStackedWidget, QApplication, QMainWindow, QWidget, QFileDialog, QLineEdit, QTableWidgetItem
from PyQt6.QtCore import QDate
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

        ## Admin Main Page
        self.open_btn.clicked.connect(self.openempdata) # Used to Open Employee data

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
                    self.stackedWidget.setCurrentWidget(self.Admin_Main_Page)
                    self.setup_Admin_Main_Page()
                elif type == "Employee":
                    pass
    
    def setup_Admin_Main_Page(self):
        # Setting up the Designation Combo Box.
        for i in self.emp_man.gen_designations():
            if i != "Login details":
                self.des_data.addItem(i)

        # Setting up the SpinBoxes
        self.l_limit.setMinimum(min(self.emp_man.find_sal_list()))
        self.u_limit.setMinimum(min(self.emp_man.find_sal_list()))
        
        self.l_limit.setMaximum(max(self.emp_man.find_sal_list()))
        self.u_limit.setMaximum(max(self.emp_man.find_sal_list()))

        self.Setup_Emp_View(self.emp_man.get_all_employees())

    def Setup_Emp_View(self, data):
        self.Emp_View.setRowCount(len(data))
        row = 0
        col = 0
        for i in data:
            col = 0
            for j in data[i]:
                self.Emp_View.setItem(row, col, QTableWidgetItem(str(data[i][j])))
                col+=1
            row+=1

    def openempdata(self):
        self.__cur_emp_ID = "E"+str(self.Emp_View.currentRow())
        self.stackedWidget.setCurrentWidget(self.Admin_EMP_Page)
        emp_data = self.emp_man.get_all_employees()[self.__cur_emp_ID]
        self.emp_name_value_ad.setText(emp_data["name"])
        self.emp_desig_value_ad.setText(emp_data["designation"])
        self.emp_salary_value_ad.setValue(emp_data["salary"])
        self.emp_gender_value_ad.setCurrentText(emp_data["gender"])
        self.emp_age_value_ad.setValue(emp_data["age"])
        self.emp_dept_value_ad.setCurrentText(emp_data["dept"])
        self.emp_exp_value_ad.setValue(emp_data["experience"])
        date = [int(i) for i in emp_data["date_of_joining"].split('-')]
        self.emp_doj_value_ad.setDate(QDate(date[-1], date[1], date[0]))

app = QApplication([])
win = Window()
win.show()
app.exec()