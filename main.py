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

        self.is_new_emp = False
        
        # Widgets

        ## Home Page
        self.opendb_btn.clicked.connect(self.openDB) # Opening A Employee DB file.
        self.newdb_btn.clicked.connect(self.newDB) # Creating a new Employee DB file.
        
        ## Login Page
        self.rand_pass_btn.clicked.connect(self.rand_pass) # Generating a random password.
        self.login_btn.clicked.connect(self.login) # Login

        ## Admin Main Page
        self.open_btn.clicked.connect(self.openempdata) # Used to Open Employee data.
        self.del_btn.clicked.connect(self.delete_emp) # Used to delete an employee.
        self.new_btn.clicked.connect(self.new_emp) # Used to create a new employee.
        self.search_btn.clicked.connect(self.search_emps) # Used to search for employees.

        ## Admin Employee View Page
        self.back_ad_btn.clicked.connect(self.loadAdmin_Page_Again) # Changes the page back to the Admin Main Page.
        self.update_ad_btn.clicked.connect(self.update_emp_details)

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
        desigs = [self.des_data.itemText(i) for i in range(self.des_data.count())]
        for i in self.emp_man.gen_designations():
            if i != "Login details" and i not in desigs:
                self.des_data.addItem(i)

        # Setting up the SpinBoxes
        sal_list = self.emp_man.find_sal_list()
        self.l_limit.setMinimum(min(sal_list))
        self.u_limit.setMinimum(min(sal_list))
        
        self.l_limit.setMaximum(max(sal_list))
        self.u_limit.setMaximum(max(sal_list))

        self.l_limit.setValue(min(sal_list))
        self.u_limit.setValue(max(sal_list))

        self.Setup_Emp_View(self.emp_man.get_all_employees())

    def Setup_Emp_View(self, emp_data_view):
        self.Emp_View.setRowCount(len(emp_data_view))
        row = 0
        col = 0
        for i in sorted(emp_data_view):
            self.Emp_View.setItem(row, 0, QTableWidgetItem(i))
            col = 1
            for j in emp_data_view[i]:
                self.Emp_View.setItem(row, col, QTableWidgetItem(str(emp_data_view[i][j])))
                col+=1
            row+=1

    # Admin Main Page
    def openempdata(self):
        
        self.stackedWidget.setCurrentWidget(self.Admin_EMP_Page) # Changing the page.
        
        # Setting up the necessary variables
        self.__cur_emp_ID = self.Emp_View.item(self.Emp_View.currentRow(), 0).text()
        emp_data = self.emp_man.get_all_employees()[self.__cur_emp_ID]

        self.emp_salary_value_ad.setMaximum(2147483647) # Changing the maximum value
        depts = [self.emp_dept_value_ad.itemText(i) for i in range(self.emp_dept_value_ad.count())]
        for i in self.emp_man.gen_departments():
            if i != "Login details" and i not in depts:
                self.emp_dept_value_ad.addItem(i)

        # Setting up the values in the widgets
        self.emp_name_value_ad.setText(emp_data["name"])
        self.emp_desig_value_ad.setText(emp_data["designation"])
        self.emp_salary_value_ad.setValue(emp_data["salary"])
        self.emp_gender_value_ad.setCurrentText(emp_data["gender"])
        self.emp_age_value_ad.setValue(emp_data["age"])
        self.emp_dept_value_ad.setCurrentText(emp_data["dept"])
        self.emp_exp_value_ad.setValue(emp_data["experience"])
        date = [int(i) for i in emp_data["date_of_joining"].split('-')]
        self.emp_doj_value_ad.setDate(QDate(date[-1], date[1], date[0]))
    
    def delete_emp(self):
        self.emp_man.remove_employee(self.Emp_View.item(self.Emp_View.currentRow(), 0).text()) # Deleting the employee
        self.setup_Admin_Main_Page() # Refreshing the data

    def new_emp(self):
        self.stackedWidget.setCurrentWidget(self.Admin_EMP_Page)
        self.is_new_emp = True

        # Widget Configurations
        self.emp_salary_value_ad.setMaximum(2147483647)
        depts = [self.emp_dept_value_ad.itemText(i) for i in range(self.emp_dept_value_ad.count())]
        for i in self.emp_man.gen_departments():
            if i != "Login details" and i not in depts:
                self.emp_dept_value_ad.addItem(i)

        # Setting the values to null of the widgets.
        self.emp_name_value_ad.setText('')
        self.emp_desig_value_ad.setText('')
        self.emp_salary_value_ad.setValue(0)
        self.emp_gender_value_ad.setCurrentText('')
        self.emp_age_value_ad.setValue(0)
        self.emp_dept_value_ad.setCurrentText('')
        self.emp_exp_value_ad.setValue(0)
        self.emp_doj_value_ad.setDate(QDate.currentDate())

    def search_emps(self):
        desig_data = self.des_data.currentText()
        if desig_data == 'All':
            desig_data = None
        search_data = self.emp_man.search(name = self.search_txt.text(), salaryl = (self.l_limit.value(), self.u_limit.value()), designation= desig_data)
        # print("search data: ", search_data)
        self.Setup_Emp_View(search_data)

    # Admin Employee View Page
    def update_emp_details(self):
        if not self.is_new_emp:
            self.emp_man.update_employee(self.__cur_emp_ID, self.emp_name_value_ad.text(), self.emp_gender_value_ad.currentText(), self.emp_salary_value_ad.value(), self.emp_desig_value_ad.text(), self.emp_doj_value_ad.date().toString('dd-MM-yyyy'), self.emp_age_value_ad.value(), self.emp_dept_value_ad.currentText(), self.emp_exp_value_ad.value())
        else:
            self.emp_man.add_employee(self.emp_name_value_ad.text(), self.emp_gender_value_ad.currentText(), self.emp_salary_value_ad.value(), self.emp_desig_value_ad.text(), self.emp_doj_value_ad.date().toString('dd-MM-yyyy'), self.emp_age_value_ad.value(), self.emp_exp_value_ad.value(), self.emp_dept_value_ad.currentText(), )
            self.is_new_emp = False        

    def loadAdmin_Page_Again(self):
        self.stackedWidget.setCurrentWidget(self.Admin_Main_Page)
        self.setup_Admin_Main_Page()

app = QApplication([])
win = Window()
win.show()
app.exec()