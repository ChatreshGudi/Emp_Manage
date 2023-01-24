# import PyQt6
from PyQt6.uic import loadUi
from PyQt6 import *
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QStackedWidget, QApplication, QMainWindow
import sys
import os

class LoginPage(QMainWindow):
    def __init__(self) -> None:
        super(LoginPage, self).__init__()
        loadUi("./UI_Files/login.ui")
        main.setCurrentIndex(0)

app = QApplication(sys.argv)
main = QStackedWidget()
login_page = LoginPage()
main.addWidget(login_page)

main.setMaximumHeight(600)
main.setMaximumWidth(1000)
main.setMinimumHeight(600)
main.setMinimumWidth(1000)

main.show()

try:
    sys.exit(app.exec())
except:
    print("Exiting")