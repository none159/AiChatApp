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
     def __init__(self,email=None,username=None,bot_name=None):
          super().__init__()
          self.email = email
          self.oldusername = username
          self.bot_name = bot_name
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
         self.Update_username.clicked.connect(self.updateusername)
         self.Update_botname = QPushButton("Update")
         self.Update_botname.clicked.connect(self.updatebotname)
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
            from home import MainChatWindow
            self.close()
            if self.bot_name != None:
                self.home_window = MainChatWindow(bot_name=self.bot_name,username=self.oldusername,trialclose=True)  
                self.home_window.show()
            else:
                self.home_window = MainChatWindow(username=self.oldusername,trialclose=True)  
                self.home_window.show()
     def updateusername(self):
        messagebox = QMessageBox()
        messagebox.setStyleSheet("""
                                 *{
                                        background-color:#222222;
                                        margin:10px;
                                                       }
                                QLabel{
                                margin:0;
                                color:white;
                                }
                                QPushButton{
                                background-color:#007FFF;
                                margin:0;
                                padding:10px;
                                color: White;
                                border:none;
                                border-radius:0.3em;
                                                       }
                                
                                """)
        connection = os.getenv("MONGODB_CONNECTION")
        cluster = MongoClient(connection)
        db = cluster["Users"]
        collection = db["User"]
        collection.update_one({"email":self.email},{"$set" : {"username":self.username.text()}})
        self.oldusername = self.username.text()
        messagebox.setIcon(QMessageBox.Information)
        messagebox.setWindowTitle("Success")
        messagebox.setText("You successfully Updated username")
        messagebox.exec_()
              
     def updatebotname(self):
        messagebox = QMessageBox()
        messagebox.setStyleSheet("""
                                 *{
                                        background-color:#222222;
                                        margin:10px;
                                                       }
                                QLabel{
                                margin:0;
                                color:white;
                                }
                                QPushButton{
                                background-color:#007FFF;
                                margin:0;
                                padding:10px;
                                color: White;
                                border:none;
                                border-radius:0.3em;
                                                       }
                                
                                """)
        connection = os.getenv("MONGODB_CONNECTION")
        cluster = MongoClient(connection)
        db = cluster["Users"]
        collection = db["Settings"]
        collection.insert_one({"email":self.email,"botname":self.botname.text()})
        self.bot_name = self.botname.text()
        messagebox.setIcon(QMessageBox.Information)
        messagebox.setWindowTitle("Success")
        messagebox.setText("You successfully Updated Botname")
        messagebox.exec_()
              
    