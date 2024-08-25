from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QLabel, QWidget, QPushButton, QVBoxLayout

class MainAboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("About Bot")
        self.setGeometry(100, 100, 500, 500)
        self.setFixedSize(self.width(), self.height())
        self.center()

        # Title
        self.label = QLabel("About Us")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)


        self.description = QLabel("This chatbot is Simple designed to help you with various tasks. "
                                  "It can provide information, assist with scheduling, and much more. "
                                  "Our mission is to make your life easier with intuitive AI solutions.")
        self.description.setWordWrap(True)
        self.description.setAlignment(QtCore.Qt.AlignCenter)
        self.description.setFont(QFont("Arial", 12))


        self.back = QPushButton("< Back")
        self.back.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.back.clicked.connect(self.goback)


        ybox = QVBoxLayout()
        ybox.addWidget(self.label)
        ybox.addWidget(self.description)
        ybox.addWidget(self.back)
        ybox.setAlignment(QtCore.Qt.AlignCenter)
        ybox.setContentsMargins(40, 40, 40, 40)  
        self.setLayout(ybox)

        # StyleSheet
        self.setStyleSheet("""
            * {
                background-color: #222222;
            }

            QLabel {
                color: White;
                margin: 10px;
            }

            QPushButton {
                background-color: #007FFF;
                padding: 10px 30px;
                margin: 20px 150px;
                color: White;
                border: none;
                border-radius: 0.3em;
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


