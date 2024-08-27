import random 
import json
import torch
import sys
from model import NeuralNet
from nltkutils import bag_of_words,tokenize
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor,QFont
from PyQt5.QtWidgets import QApplication, QWidget,QDesktopWidget,QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
from cryptography.fernet import Fernet
with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE,weights_only=True)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]
class MainChatWindow(QWidget):
     def __init__(self, username="Me", trialclose=False,email=None,bot_name="AI"):
          super().__init__()
          self.username = username.capitalize() 
          self.trialclose = trialclose
          self.email = email
          self.bot_name = bot_name
          self.initUI()
     
     def initUI(self):
         self.setWindowTitle("Chatbot")
         self.setGeometry(180, 150, 600, 600)
         self.setFixedSize(self.width(), self.height())
         self.center()
         
         self.output_log = QTextEdit()
         self.output_log.setReadOnly(True)
         self.input = QLineEdit()
         
         font = QFont()
         font.setPointSize(12)
         self.output_log.setFont(font)
         
         self.setting = QPushButton("Settings", self)
         self.setting.setDisabled(True)
         self.setting.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         self.setting.setFixedSize(80, 40)
         self.setting.setStyleSheet("""
         QPushButton {
             background-color: #007FFF;
             color: white;
             border-radius: .3em;
             border: none;
         }
         """)
         self.setting.clicked.connect(self.settingwindow)
         self.check_trial()
         
         self.btn_submit = QPushButton("Submit")
         self.btn_submit.clicked.connect(self.enter)
         self.btn_submit.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
         
         self.input.returnPressed.connect(self.enter)
         
         top_layout = QHBoxLayout()
         top_layout.addWidget(self.setting)
         top_layout.addStretch(1)
         
         bottom_layout = QHBoxLayout()
         bottom_layout.addWidget(self.input)
         bottom_layout.addWidget(self.btn_submit)
         
         main_layout = QVBoxLayout()
         main_layout.addLayout(top_layout)
         main_layout.addWidget(self.output_log)
         main_layout.addLayout(bottom_layout)
         
         self.setLayout(main_layout)
         
         self.setStyleSheet("""
            * {
                background-color: #222222;
            }
            QTextEdit {
                background-color: #28282B;
                color: white;
                border: none;
                border-radius: 0.2em;
                outline: none;
            }
            QLineEdit {
                padding: 10px;
                background-color: #28282B;
                color: white;
                border: none;
                border-radius: .3em;
            }
            QPushButton {
                padding: 10px;
                background-color: #007FFF;
                color: white;
                border-radius: .3em;
                border: none;
            }
        """)
         
     def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2,
                  (screen.height() - size.height()) // 2)
     
     def check_trial(self):
         if self.trialclose:
             self.setting.setDisabled(False)
         else:
             self.setting.setDisabled(True)
     
     def settingwindow(self):
         from settings import MainsettingWindow
         self.close()  
         self.home_window = MainsettingWindow(email=self.email,username=self.username,bot_name=self.bot_name)  
         self.home_window.show() 
     
     def enter(self):
       if self.input.text() != "":
            self.output_log.append(f"<span style='color:#50C878'>{self.username} :</span> {self.input.text()}")
            model = NeuralNet(input_size, hidden_size, output_size).to(device)
            model.load_state_dict(model_state)
            model.eval()
            
    
            sentence = self.input.text()
            sentence = tokenize(sentence)
            x = bag_of_words(sentence, all_words)
            x = x.reshape(1, x.shape[0])
            x = torch.from_numpy(x).to(device)
            
            output = model(x)
            _, predicted = torch.max(output, dim=1)
            tag = tags[predicted.item()]
            
            probs = torch.softmax(output, dim=1)
            prob = probs[0][predicted.item()]
            self.input.setText("")
            
            if prob.item() > 0.75:
                for intent in intents["intents"]:
                    if tag == intent["tag"]:
                        self.output_log.append(f"<span style='color:yellow'>{self.bot_name} :</span> {random.choice(intent['responses'])}")
            else:
                self.output_log.append(f"<span style='color:yellow'>{self.bot_name} :</span> I'm not sure I understand. Can you try asking in a different way?")
