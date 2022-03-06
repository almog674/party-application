from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout, QGroupBox, QLabel, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtGui import QIcon, QPixmap, QColor

class Message_button(QWidget):
    def __init__(self, text, icon, function):
        super().__init__() 
        self.icon = icon
        self.text = text
        self.function = function
        self.UI()

    def making_window(self):
        self.setFixedSize(80, 35)
        self.setStyleSheet('''
            background-color: #9764c7;
        ''')
        self.mouseReleaseEvent = self.function
        self.setCursor(Qt.PointingHandCursor)


    def making_shadow(self):
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setYOffset(3)
        self.shadow.setXOffset(3)
        self.shadow.setBlurRadius(15)
        self.setGraphicsEffect(self.shadow)

    def initializing_container(self):
        self.container = QHBoxLayout()
        self.container.setSpacing(0)
        self.container.setContentsMargins(QMargins(0,0,0,0))


    
    def making_label(self):
        self.text_label = QLabel(self.text)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet('''
        QLabel {
            font-size: 16px;
            font-family: sans-serif;
            font-weight: 600;
            padding-left: 10px;
            border-bottom-left-radius: 8px;
            border-top-left-radius: 8px;
        }
        ''')

    def making_icon(self):
        self.icon_label = self.make_icon(self.icon, 15, 15)
        self.icon_label.setStyleSheet('''
        QLabel {
            border-bottom-right-radius: 8px;
            border-top-right-radius: 8px;
        }
        ''')

    def UI(self):
        self.making_window()
        self.making_shadow()
        self.initializing_container()
        self.making_label()
        self.making_icon()

        self.container.addWidget(self.text_label)
        self.container.addWidget(self.icon_label)
        
        self.setLayout(self.container)
        self.show()


    def make_icon(self, url, width, height):
        icon_container = QLabel()
        icon_container.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(url)
        pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio)
        icon_container.setPixmap(pixmap)
        # mask = icon.createMaskFromColor(QColor('black'), Qt.MaskOutColor)
        #     icon.fill(QColor(color))
        #     icon.setMask(mask)
        return icon_container

