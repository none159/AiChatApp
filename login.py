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
class MainloginWindow(QWidget):
     def __init__(self):
          super().__init__()
          self.initUI()
     def initUI(self):
         self.setWindowTitle("Login")
         self.setGeometry(100,100,500,500)
         self.setFixedSize(self.width(),self.height())
         self.center()
         self.label = QLabel("Login")
         self.email = QLineEdit()
         self.email.setPlaceholderText("Email....")
         self.password = QLineEdit()
         self.password.setPlaceholderText("Password....")
         self.password.setEchoMode(QLineEdit.Password)
         self.login = QPushButton("Login")
         self.login.clicked.connect(self.log)
         self.back = QPushButton("<",self)
         self.back.clicked.connect(self.goback)
         self.back.setGeometry(-11, -11, 60, 60)
         self.back.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         font = QFont()
         font.setPointSize(15)
         self.label.setFont(font)
         self.login.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         ybox = QVBoxLayout()
         ybox.addWidget(self.label)
         ybox.addWidget(self.email)
         ybox.addWidget(self.password)
         ybox.addWidget(self.login)
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
     def log(self):
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
       regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
       if self.email.text() != ""  and self.password.text() != "":
          if re.fullmatch(regex,self.email.text()):
               if(len(self.password.text())<6):
                   messagebox.setIcon(QMessageBox.Warning)
                   messagebox.setWindowTitle("Invalid Password")
                   messagebox.setText("Your password must be 6 caracters or more")
                   messagebox.exec_()
               else: 
                    connection = os.getenv("MONGODB_CONNECTION")
                    cluster = MongoClient(connection)
                    db = cluster["Users"]
                    collection = db["User"] 
                    collection2 = db["Settings"]
                    user = {"email":self.email.text().lower(),"password":self.password.text()}
                    result = collection.find_one({"email":user["email"]})
                    result2 = collection2.find_one({"email":user["email"]})
                    if result and bcrypt.checkpw(self.password.text().encode('utf-8'), result["password"]):
                              user = {"username":result["username"],"email":result["email"],"password":result["password"]}
                              messagebox.setIcon(QMessageBox.Information)
                              messagebox.setWindowTitle("Success")
                              messagebox.setText("You successfully Logged in")
                              messagebox.exec_()
                              self.close()  
                              if result2:
                                   self.home_window = MainChatWindow(username=result["username"],trialclose=True,email=result["email"],bot_name=result2["botname"])  
                                   self.home_window.show()
                              else:
                                   self.home_window = MainChatWindow(username=result["username"],trialclose=True,email=result["email"])  
                                   self.home_window.show()
                    else:
                              messagebox.setIcon(QMessageBox.Information)
                              messagebox.setWindowTitle("Invalid User")
                              messagebox.setText("User Not Found Try to Signup")
                              messagebox.exec_()
                              
          else: 
                   messagebox.setIcon(QMessageBox.Warning)
                   messagebox.setWindowTitle("Invalid Email")
                   messagebox.setText("Your email is invalid")
                   messagebox.exec_()
           
       else:
           messagebox.setIcon(QMessageBox.Warning)
           messagebox.setWindowTitle("Fill Form")
           messagebox.setText("Fill the form to signup")
           messagebox.exec_()