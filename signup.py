import sys
import re
import pymongo.errors
from chat import MainChatWindow
from PyQt5 import QtWidgets
from dotenv import load_dotenv
import os
import bcrypt
import pymongo
from login import MainloginWindow
from pymongo import MongoClient
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor,QFont
from PyQt5.QtWidgets import QApplication,QMessageBox,QDesktopWidget,QLabel,QMainWindow, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout 
load_dotenv()
class MainsignupWindow(QWidget):
     def __init__(self):
          super().__init__()
          self.initUI()
     def initUI(self):
         self.setWindowTitle("signup")
         self.setGeometry(100,100,500,500)
         self.setFixedSize(self.width(),self.height())
         self.center()
         self.label = QLabel("signup")
         self.username = QLineEdit()
         self.username.setPlaceholderText("Username....")
         self.email = QLineEdit()
         self.email.setPlaceholderText("Email....")
         self.password = QLineEdit()
         self.password.setPlaceholderText("Password....")
         self.password.setEchoMode(QLineEdit.Password)
         self.sign = QPushButton("signup")
         self.sign.clicked.connect(self.signup)
         self.back = QPushButton("<",self)
         self.back.clicked.connect(self.goback)
         self.back.setGeometry(-11, -11, 60, 60)
         self.back.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         font = QFont()
         font.setPointSize(15)
         self.label.setFont(font)
         self.sign.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         ybox = QVBoxLayout()
         ybox.addWidget(self.label)
         ybox.addWidget(self.username)
         ybox.addWidget(self.email)
         ybox.addWidget(self.password)
         ybox.addWidget(self.sign)
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
     def signup(self):
       self.sign.setCursor(QCursor(QtCore.Qt.WaitCursor))
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
       if self.username.text() != "" and self.username.text() != "" and (self.password.text() != ""):
          if re.fullmatch(regex,self.email.text()):
               if(len(self.password.text())<6 or not re.search("[a-z]", self.password.text()) or not re.search("[A-Z]", self.password.text()) or not re.search("[0-9]", self.password.text()) or not re.search("[@#$%^&+=]", self.password.text())):
                   QApplication.restoreOverrideCursor()
                   messagebox.setIcon(QMessageBox.Warning)
                   messagebox.setWindowTitle("Invalid Password")
                   messagebox.setText("Your password must be 6 caracters or more and more secure")
                   messagebox.exec_()
               else: 
                    connection = os.getenv("MONGODB_CONNECTION")
                    cluster = MongoClient(connection)
                    db = cluster["Users"]
                    collection = db["User"]
                    salt = bcrypt.gensalt()
                    hashed_password = bcrypt.hashpw(self.password.text().encode('utf-8'), salt)
                    user = {"username":self.username.text().lower(),"email":self.email.text().lower(),"password":hashed_password}
                    try:
                        
                         collection.insert_one(user)
                         messagebox.setIcon(QMessageBox.Information)
                         messagebox.setWindowTitle("Success")
                         messagebox.setText("You successfully Signup.Redirecting to Login Menu...")
                         QApplication.restoreOverrideCursor()
                         messagebox.exec_()
                         self.close()  
                         self.home_window = MainloginWindow()  
                         self.home_window.show()
                    except pymongo.errors.DuplicateKeyError:
                         QApplication.restoreOverrideCursor()
                         messagebox.setIcon(QMessageBox.Warning)
                         messagebox.setWindowTitle("Duplicate")
                         messagebox.setText("Email or Username or Both already exist.")
                         messagebox.exec_()
          else:   
                   QApplication.restoreOverrideCursor()
                   messagebox.setIcon(QMessageBox.Warning)
                   messagebox.setWindowTitle("Invalid Email")
                   messagebox.setText("Your email is invalid")
                   messagebox.exec_()
           
       else:
           QApplication.restoreOverrideCursor()
           messagebox.setIcon(QMessageBox.Warning)
           messagebox.setWindowTitle("Fill Form")
           messagebox.setText("Fill the form to signup")
           messagebox.exec_()
           
