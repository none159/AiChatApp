import sys
import os
from pymongo import MongoClient
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QFileDialog, QDesktopWidget
from PyQt5.QtGui import QCursor, QFont, QPixmap
from PyQt5.QtCore import Qt
from dotenv import load_dotenv

load_dotenv()

class MainsettingWindow(QWidget):
    def __init__(self, email=None, username=None, bot_name=None):
        super().__init__()
        self.email = email
        self.oldusername = username
        self.bot_name = bot_name
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Setting")
        self.setGeometry(100, 100, 500, 500)
        self.setFixedSize(self.width(), self.height())
        self.center()

        # Profile Picture QLabel
        self.profile_pic = QLabel(self)
        self.profile_pic.setGeometry(200, 50, 100, 100)
        self.profile_pic.setStyleSheet("border: 2px solid #007FFF;")
        self.profile_pic.setAlignment(Qt.AlignCenter)

        # Upload Button
        self.upload_button = QPushButton("Upload Profile Picture", self)
        self.upload_button.setGeometry(150, 170, 200, 40)
        self.upload_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.upload_button.clicked.connect(self.upload_profile_pic)

        # Settings Label
        self.label = QLabel("Settings", self)
        font = QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setGeometry(200, 20, 100, 30)

        # Username Input and Update Button
        self.username = QLineEdit(self)
        self.username.setPlaceholderText("Enter New Username....")
        self.username.setGeometry(50, 250, 300, 40)
        self.Update_username = QPushButton("Update", self)
        self.Update_username.setGeometry(360, 250, 80, 40)
        self.Update_username.setCursor(QCursor(Qt.PointingHandCursor))
        self.Update_username.clicked.connect(self.updateusername)

        # Bot Name Input and Update Button
        self.botname = QLineEdit(self)
        self.botname.setPlaceholderText("Enter New Bot Name....")
        self.botname.setGeometry(50, 310, 300, 40)
        self.Update_botname = QPushButton("Update", self)
        self.Update_botname.setGeometry(360, 310, 80, 40)
        self.Update_botname.setCursor(QCursor(Qt.PointingHandCursor))
        self.Update_botname.clicked.connect(self.updatebotname)

        # Back Button
        self.back = QPushButton("<", self)
        self.back.setGeometry(10, 10, 40, 40)
        self.back.setCursor(QCursor(Qt.PointingHandCursor))
        self.back.clicked.connect(self.goback)

        # Load existing profile picture if available
        self.load_existing_profile_pic()

        self.setStyleSheet("""
      *{
         background-color: #222222;
      }

      QLabel{
         color: white;
         margin: 10px 200px;
      }

      QLineEdit{
         background-color: white;
        
         border-radius: 0.3em;
         color: black; 
      }

      QPushButton{
         background-color: #007FFF;
       
         color: white;
         
         border-radius: 0.3em;
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
        if self.bot_name is not None:
            self.home_window = MainChatWindow(bot_name=self.bot_name, username=self.oldusername, trialclose=True)  
            self.home_window.show()
        else:
            self.home_window = MainChatWindow(username=self.oldusername, trialclose=True)  
            self.home_window.show()

    def load_existing_profile_pic(self):
        try:
            with open("profile_pic.txt", "r") as file:
                file_path = file.read().strip()
                print(f"Loading profile picture from: {file_path}")
                self.profile_pic.setPixmap(QPixmap(file_path).scaled(
                    self.profile_pic.width(),
                    self.profile_pic.height(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                ))
        except FileNotFoundError:
            print("profile_pic.txt not found.")

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
        collection.update_one({"email": self.email}, {"$set": {"username": self.username.text()}})
        self.oldusername = self.username.text()
        messagebox.setIcon(QMessageBox.Information)
        messagebox.setWindowTitle("Success")
        messagebox.setText("You successfully updated the username")
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
        collection.insert_one({"email": self.email, "botname": self.botname.text()})
        self.bot_name = self.botname.text()
        messagebox.setIcon(QMessageBox.Information)
        messagebox.setWindowTitle("Success")
        messagebox.setText("You successfully updated the bot name")
        messagebox.exec_()

    def upload_profile_pic(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose Profile Picture", "", "Images (*.png *.jpg *.jpeg)", options=options)
        if file_path:
            self.profile_pic.setPixmap(QPixmap(file_path).scaled(
                self.profile_pic.width(),
                self.profile_pic.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))
            self.save_profile_pic(file_path)

    def save_profile_pic(self, file_path):
        with open("profile_pic.txt", "w") as file:
            file.write(file_path)
