# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 19:08:52 2020

@author: Yu Zhe
"""
#pyqt doesn't run twice on juoyter& spyder, C++ library not designed to run on interactive notebook
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QComboBox, QLabel, QLineEdit, \
    QHBoxLayout, QTableView, QTabWidget, QMainWindow
from PyQt5 import QtGui, QtCore

def main_GUI():
    app = QApplication([])
    window = QWidget()
    vBox = QVBoxLayout()

    # Username
    username = QLineEdit("John Doe")
    vBox.addWidget(QLabel("Username"))
    vBox.addWidget(username)

    # Password
    pw = QLineEdit()
    pw.setEchoMode(QLineEdit.Password)
    vBox.addWidget(QLabel("Password"))
    vBox.addWidget(pw)

    login_btn = QPushButton('Login')
    def login_func(): #Function when process button is clicked
        print(username.text())
        print(pw.text())    
    login_btn.clicked.connect(login_func)
    vBox.addWidget(login_btn)
     
    window.setLayout(vBox)
    window.setWindowTitle('Login Page')
    window.show()
    app.exec_()
    

main_GUI()

"""
python pyinstaller.py --noconsole --onefile yourscript.py
"""