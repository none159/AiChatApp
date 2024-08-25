"""
Add settings to the bot :
- Change Bot Name
- Change Username
- You're Level
- Change Badge 
- Change Title
!!! in progress !!!
"""
import sys
import re
import pymongo
from pymongo import MongoClient
from chat import MainChatWindow
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import os
from dotenv import load_dotenv
import bcrypt
from PyQt5.QtGui import QCursor,QFont
from PyQt5.QtWidgets import QApplication,QMessageBox,QDesktopWidget,QLabel,QMainWindow, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout
load_dotenv()
class MainsettingWindow(QWidget):
     def __init__(self):
          super().__init__()
          self.initUI()
     def initUI(self):
         self.setWindowTitle("Setting")
         self.setGeometry(100,100,500,500)
         self.setFixedSize(self.width(),self.height())
         self.center()
         self.label = QLabel("Settings")
         self.username = QLineEdit()
         self.username.setPlaceholderText("Enter New Username....")
         self.botname = QLineEdit()
         self.botname.setPlaceholderText("Enter New Bot Name....")
         self.Update_username = QPushButton("Update")
         self.Update_botname = QPushButton("Update")
         self.back = QPushButton("<",self)
         self.back.clicked.connect(self.goback)
         self.back.setGeometry(-11, -11, 60, 60)
         self.back.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         font = QFont()
         font.setPointSize(15)
         self.label.setFont(font)
         self.Update_username.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         self.Update_botname.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         xbox1 = QHBoxLayout()
         xbox2 = QHBoxLayout()
         ybox = QVBoxLayout()
         ybox.addWidget(self.label)
         xbox1.addWidget(self.username)
         xbox1.addWidget(self.Update_username)
         xbox2.addWidget(self.botname)
         xbox2.addWidget(self.Update_botname)
         ybox.addLayout(xbox1)
         ybox.addLayout(xbox2)
         ybox.setAlignment(QtCore.Qt.AlignCenter)
         self.setLayout(ybox)
         self.setStyleSheet("""
          *{
              background-color:#222222;
                            }

        QLabel{
             color:White;   
             margin:10px 200px;  
                            }
        QLineEdit{
                background-color:White;
                padding:10px 0;
                margin:10px;   
                outline:none;
                border:none;
                border-radius:0.3em;         
                            }
         QPushButton{
            background-color:#007FFF;
            padding:10px 50px;
            margin:10px;
            color: White;
            border:none;
            border-radius:0.3em;

                            }
        """)
     def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2,
                  (screen.height() - size.height()) // 2)
     def goback(self):
            from home import MainHomeWindow
            self.close()  
            self.home_window = MainHomeWindow()  
            self.home_window.show()
    