# importing libraries
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(150, 250, 350, 350)
        self.setWindowTitle("Learn how to use Labels")
        self.UI()


    def UI(self):
        self.button_container = QHBoxLayout()
        self.button_container_box = QGroupBox()
        
        self.button_container_box.setFixedSize(200,60)
        self.button_container_box.setStyleSheet('''QGroupBox {
            padding: 0px;
            margin: 0px
            border-bottom-left-radius: 15px;
            }
        ''')
        self.button_container_box.setLayout(self.button_container)
        

        self.icon = QLabel()
        self.button = QPushButton('Send Email')

        self.button.stackUnder(self.icon)
        self.icon.stackUnder(self.icon)
        self.button.setFixedSize(200,60)
        self.button.setStyleSheet('''QPushButton {
            background-color: #017158;
            font-size: 18px;
            color: #fafafa;
            }
        ''')

        self.icon.setFixedWidth(60)
        image = QPixmap('player_icons\email-icon.svg')
        image = image.scaled(35,35, Qt.KeepAspectRatio)
        self.icon.setPixmap(image)
        self.icon.setAlignment(QtCore.Qt.AlignCenter)
        self.icon.setStyleSheet('''QLabel {
            background-color: #FEFEFE;
            font-size: 18;
            border-bottom-left-radius: 25px;
            border-top-right-radius: 25px;
            }
        ''')
        self.button_container.setContentsMargins(QMargins(0,0,0,0))
        self.button_container.addWidget(self.icon, alignment = QtCore.Qt.AlignLeft)
        self.button_container.addWidget(self.button)

        self.main_layout = QVBoxLayout()
        self.main_layout_box = QGroupBox()
        self.main_layout_box.setLayout(self.main_layout)
        self.main_layout_box.setStyleSheet('''QGroupBox {
            background-color: #86B3B9;
            font-size: 18;
            }
        ''')
        self.main_layout_box.setAlignment(QtCore.Qt.AlignCenter)

        self.main_layout.addWidget(self.button_container_box, alignment = QtCore.Qt.AlignCenter)
        self.setStyleSheet(('''QWidget {
            background-color: #86B3B9;
            font-size: 18;
            padding: 0px;
            margin: 0px;
            }
        '''))
        self.setLayout(self.main_layout)

        self.show()

def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()