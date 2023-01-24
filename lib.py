import json
import random
import datetime
import os

class EmployeeManagement:
    def __init__(self, filepath):
        self.filepath = filepath
        if os.path.isfile(self.filepath):
            self.__file_read = open(self.filepath, 'r')
        else:
            file = open(self.filepath, 'w')
            self.__file_read = open(self.filepath, 'r')
            file.close()
        if self.__file_read.read() != "":
            self.__file_read.seek(0)
            self.__employee_data = json.loads(self.__file_read.read().strip())
        self.__employee_data = {}

    def add_employee(self, name:str, gender:str, salary:int, designation:str, date_of_joining:datetime, age:int, exp:int, dept:str):
        employee_id = self.__generate_employee_id()
        self.__employee_data[employee_id] = {
            "name": name,
            "gender": gender,
            "salary": salary,
            "designation": designation,
            "date_of_joining": date_of_joining,
            "age": age,
            "experience":exp,
            "dept":dept
        }
        self.update_file()
        return employee_id

    def remove_employee(self, employee_id):
        if employee_id in self.__employee_data:
            del self.__employee_data[employee_id]
            self.update_file()
            return True
        else:
            return False

    def update_employee(self, employee_id, name=None, gender=None, salary=None, designation=None, date_of_joining=None):
        if employee_id in self.__employee_data:
            if name:
                self.__employee_data[employee_id]["name"] = name
            if gender:
                self.__employee_data[employee_id]["gender"] = gender
            if salary:
                self.__employee_data[employee_id]["salary"] = salary
            if designation:
                self.__employee_data[employee_id]["designation"] = designation
            if date_of_joining:
                self.__employee_data[employee_id]["date_of_joining"] = date_of_joining
            self.update_file()
            return True
        else:
            return False

    def search(self, employee_id:str = None, name:str = None, salaryl:tuple = None, designation:str = None, date_of_joining = None):
        if employee_id in self.__employee_data:
            return self.__employee_data[employee_id]
        else:
            return None

    def get_all_employees(self):
        '''Returns the employee data.'''
        return self.__employee_data

    def __generate_employee_id(self):
        '''Generate a unique employee id'''
        return "E" + str(len(self.__employee_data) + 1)
    
    def update_file(self):
        '''Writes data to the file.'''
        with open(self.filepath, 'w') as fwrite:
            fwrite.write(json.dumps(self.__employee_data))

emp_man = EmployeeManagement("emp.json")
emp_man.add_employee("Chatresh", "M", 100000, "Developer", "12-12-2023", 16, 2, "Research")
emp_man.add_employee("Avinash", "M", 1000000, "CEO", "12-12-2023", 18, 2, "Management")
emp_man.remove_employee("E2")
emp_man.update_employee("E1", salary = 1000000000000)
print(emp_man.get_all_employees())
