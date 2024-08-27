import sys
from chat import MainChatWindow
from PyQt5 import QtWidgets
from dotenv import load_dotenv
from login import MainloginWindow
from about import MainAboutWindow
from signup import MainsignupWindow
from PyQt5 import QtCore
import os
from datetime import datetime,timedelta
from PyQt5.QtGui import QCursor,QFont
from PyQt5.QtWidgets import QApplication,QMessageBox,QDesktopWidget,QLabel,QMainWindow, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout
from cryptography.fernet import Fernet
load_dotenv()
TRIAL_DAYS = 1
TRIAL_FILE = "trial_info.enc"
TRIAL_KEY = os.getenv('TRIAL_KEY')

class MainHomeWindow(QMainWindow):
     def __init__(self):
          super().__init__()
          self.chat_window = None
          self.signup_window = None
          self.login_window = None
          self.trialopen = False
          self.about_window = None
          self.initUI()
     def initUI(self):
         self.setWindowTitle("Chatbot")
         self.setGeometry(100,100,500,500)
         self.center()
         self.setFixedSize(self.width(),self.height())
         self.label = QLabel("Welcome To Chatbot")
         self.signup = QPushButton("Signup")
         self.login = QPushButton("Login")
         self.freetrial = QPushButton("Try The Bot")
         self.about = QPushButton("About The Bot")
         self.mainwidget = QtWidgets.QWidget(self)
         self.setCentralWidget(self.mainwidget)
         font = QFont()
         font.setPointSize(13)
         self.label.setFont(font)
         self.login.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         self.signup.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         self.freetrial.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         self.about.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         self.freetrial.clicked.connect(self.chatwindow)
         self.login.clicked.connect(self.loginwindow)
         self.signup.clicked.connect(self.signupwindow)
         self.about.clicked.connect(self.aboutwindow)
         ybox = QVBoxLayout(self.mainwidget)
         ybox.addWidget(self.label)
         ybox.addWidget(self.signup)
         ybox.addWidget(self.login)
         ybox.addWidget(self.freetrial)
         ybox.addWidget(self.about)
         ybox.setAlignment(QtCore.Qt.AlignCenter)

         self.setStyleSheet("""
          *{
              background-color:#222222;

                            }

        QLabel{
             color:White;   
             margin:0 auto;   
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
     def encrypt_data(self,data):
         self.trialopen=True
         fernet = Fernet(os.getenv("TRIAL_KEY").encode())
         encrypted_data = fernet.encrypt(data.encode())
         return encrypted_data
     def decrypt_data(self,encrypted_data):
         TRIAL_KEY = os.getenv("TRIAL_KEY")
         fernet = Fernet(TRIAL_KEY.encode())
         decrypted_data = fernet.decrypt(encrypted_data).decode()
         return decrypted_data
     def check_trial(self):
          if os.path.exists(TRIAL_FILE):
             with open(TRIAL_FILE,"rb") as f:
                 self.encrypted_data = f.read()
             start_date = datetime.fromisoformat(self.decrypt_data(self.encrypted_data))
             if datetime.now() - start_date > timedelta(days=TRIAL_DAYS):
                 self.trial_expired()
             else:
                 self.trialopen = True
                 days_left = TRIAL_DAYS - (datetime.now()-start_date).days
                 QMessageBox.information(self,"Free Trial",f"You have {days_left} days left in your free trial")
          else:
              self.start_trial()
     def trial_expired(self):
         self.trialopen=False
         QMessageBox.warning(self,"Trial Expired","Your free trial has expired signup to continue Chatting")
     def start_trial(self):
         start_date = datetime.now().isoformat()
         encrypted_date = self.encrypt_data(start_date)
         with open(TRIAL_FILE,"wb") as f:
             f.write(encrypted_date)
         QMessageBox.information(self,"Free Trial",f"Your Free Trial has started.You Have {TRIAL_DAYS} days")
     def chatwindow(self):
         self.check_trial()
         if self.chat_window is None and self.trialopen:
          self.chat_window = MainChatWindow(trialclose=not self.trialopen)
          self.chat_window.show()
          self.chat_window.raise_()
          self.close()
     def loginwindow(self):
         if self.login_window is None :
          self.chat_window = MainloginWindow()
          self.chat_window.show()
          self.chat_window.raise_()
          self.close()
     def signupwindow(self):
         if self.signup_window is None :
          self.chat_window = MainsignupWindow()
          self.chat_window.show()
          self.chat_window.raise_()
          self.close()
     def aboutwindow(self):
         if self.about_window is None :
          self.chat_window = MainAboutWindow()
          self.chat_window.show()
          self.chat_window.raise_()
          self.close()
     
     
    
def main():
     app = QApplication(sys.argv)
     window = MainHomeWindow()
     window.show()
     result =  app.exec_()
     sys.exit(result)
           
            
if __name__ == '__main__':
     main()