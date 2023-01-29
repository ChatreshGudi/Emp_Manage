import json
import random
import datetime
import os
import random
from string import *

def random_pas_gen():
    return ''.join(random.sample(ascii_lowercase + ascii_uppercase + digits + punctuation, 8))

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
        else:
            self.__employee_data = {"Login details":{"Admin":{}, "Employee":{}}}
    
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
        self.__employee_data["Login details"]["Employee"][name] = employee_id+gender
        self.update_file()
        return employee_id

    def remove_employee(self, employee_id):
        if employee_id in self.__employee_data:
            del_emp_name = ""
            for k in self.__employee_data["Login details"]["Employee"]:
                if self.__employee_data["Login details"]["Employee"][k][:-1] == employee_id:
                    del_emp_name = k
            del self.__employee_data["Login details"]["Employee"][del_emp_name]
            del self.__employee_data[employee_id]
            num = int(employee_id[1:])
            for i in range(num, len(self.__employee_data)-1):
                self.__employee_data["E"+str(i)] = self.__employee_data["E"+str(i+1)]
            if len(self.__employee_data)-1 != int(employee_id[1:]):
                del self.__employee_data["E"+str(len(self.__employee_data)-2)]
            self.update_file()
            return True
        else:
            return False

    def update_employee(self, employee_id, name=None, gender=None, salary=None, designation=None, date_of_joining=None, age = None, dept = None, exp = None):
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
            if age:
                self.__employee_data[employee_id]["age"] = age
            if dept:
                self.__employee_data[employee_id]["dept"] = dept
            if exp:
                self.__employee_data[employee_id]["experience"] = exp
            self.update_file()
            return True
        else:
            return False

    def search(self, employee_id:str = None, name:str = None, salaryl:tuple = None, designation:str = None):
        ids = set()
        if employee_id:
            ids.add(employee_id)
        if name: # Searching Based on Name
            for i in self.__employee_data:
                if i != "Login details":
                    if name in self.__employee_data[i]["name"]:
                        ids.add(i)
        
        if salaryl: # Searching Based on Salary
            if len(ids) == 0:
                for i in self.__employee_data:
                    if i != "Login details":
                        if self.__employee_data[i]["salary"] in range(salaryl[0], salaryl[1]+1):
                            ids.add(i)
            else:
                samp_sal_ids = ids.copy()
                for i in ids:
                    if self.__employee_data[i]["salary"] not in range(salaryl[0], salaryl[1]+1):
                            samp_sal_ids.remove(i)
                ids = samp_sal_ids
                del samp_sal_ids
            
        if designation: # Searching Based on designation.
            if len(ids) == 0:
                for i in self.__employee_data:
                    if i != "Login details":
                        if self.__employee_data[i]["designation"] == designation:
                            ids.add(i)
            else:
                samp_desig_ids = ids.copy()
                for i in ids:
                    if self.__employee_data[i]["designation"] != designation:
                        samp_desig_ids.remove(i)
                ids = samp_desig_ids
                del samp_desig_ids
        
        data = {}
        for i in ids:
            data[i] = self.__employee_data[i]
        return data
            
    def get_all_employees(self):
        '''Returns the employee data.'''
        data = self.__employee_data.copy()
        del data["Login details"]
        return data

    def __generate_employee_id(self):
        '''Generate a unique employee id'''
        return "E" + str(len(self.__employee_data)-1)
    
    def update_file(self):
        '''Writes data to the file.'''
        with open(self.filepath, 'w') as fwrite:
            fwrite.write(json.dumps(self.__employee_data))

    def gen_designations(self):
        designations = set()
        for i in self.__employee_data:
            if i != "Login details":
                designations.add(self.__employee_data[i]["designation"])
        return designations

    def gen_departments(self):
        departments = set()
        for i in self.__employee_data:
            if i != "Login details":
                departments.add(self.__employee_data[i]["dept"])
        return departments

    def find_sal_list(self):
        sal_list = []
        for i in self.__employee_data:
            if i!= "Login details":
                sal_list.append(self.__employee_data[i]["salary"])
        if len(sal_list) == 0:
            return [0]
        return sal_list
    
    def verify_login(self, type:str, name:str, passw:str):
        if name in self.__employee_data["Login details"][type] and self.__employee_data["Login details"][type][name] == passw:
            return True
        return False
    
    def register_admin(self, uname:str, upass:str):
        self.__employee_data["Login details"]["Admin"][uname] = upass
        self.update_file()

# Testing

# emp_man = EmployeeManagement("emp.json")
# emp_man.register_admin("admin", "password")
# emp_man.verify_login("Admin", "ad", "pass")
# emp_man.add_employee("Chatresh", "M", 100000, "Developer", "12-12-2023", 16, 2, "Research")
# emp_man.add_employee("Avinash", "M", 1000000, "CEO", "12-12-2023", 18, 2, "Management")
# emp_man.remove_employee("E3")
# emp_man.update_employee("E1", salary = 1000000000000)
# print(emp_man.search(salaryl=(100000, 9999990)))
# print(emp_man.get_all_employees())
