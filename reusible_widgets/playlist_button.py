from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout, QGroupBox, QLabel, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QMargins, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QColor


class Playlist_Button(QWidget):
    def __init__(self, icon, function, size = 40, color = '#ff0000'):
        super().__init__()
        self.icon = icon
        self.function = function
        self.size = size
        self.UI()

    def making_window(self):
        self.setContentsMargins(QMargins(0,0,0,0))
        self.setStyleSheet(f'''
            background-color: #242424;
            border-radius: {(self.size / 2) - 1};
        ''')
        self.setFixedSize(self.size, self.size)
        self.setCursor(Qt.PointingHandCursor)
        self.mouseReleaseEvent = self.function
        self.add_shadow(widget = self, x = 0, y = 0 , blur = (self.size / 4), color = '#fff')

    def initializing_container(self):
        self.main_layout = QHBoxLayout()
        self.main_layout.mouseReleaseEvent = self.function
        self.main_layout.setContentsMargins(QMargins(0,0,0,0))

    def build_icon_container(self):
        self.icon_container = self.make_icon(self.icon, (self.size / 2), (self.size / 2), color = '#ff0000')
        self.icon_container.setFixedSize(self.size, self.size)
        self.icon_container.clicked.connect(self.function)
        self.icon_container.setStyleSheet(f'''
            border-radius: {(self.size / 2) - 1};
            border: 2px solid black;
        ''')

    def mouseReleaseEvent(self, e):
        self.function

    def UI(self):
        # The UI Functions of the component
        self.making_window()
        self.initializing_container()
        self.build_icon_container()

        self.main_layout.addWidget(self.icon_container)
        self.setLayout(self.main_layout)

    def add_shadow(self, widget, x, y, blur, color = '#000'):
        shadow = QGraphicsDropShadowEffect()
        shadow.setYOffset(y)
        shadow.setXOffset(x)
        shadow.setBlurRadius(blur)
        shadow.setColor(QColor(color))
        widget.setGraphicsEffect(shadow)
        return widget

    def update_heart_icon(self, full):
        icon = QPixmap('player_icons\heart-icon.svg')
        if full == True:
            icon = QPixmap('player_icons\heart-full-icon.svg')
        mask = icon.createMaskFromColor(QColor('black'), Qt.MaskOutColor)
        icon.fill(QColor('red'))
        icon.setMask(mask)
        self.icon_container.setIcon(QIcon(icon))
        
    def make_icon(self, url, width, height, color = None):
        icon_container = QPushButton()
        pixmap = QPixmap(url)
        pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio)
        if color != None:
            mask = pixmap.createMaskFromColor(QColor('black'), Qt.MaskOutColor)
            pixmap.fill(QColor(color))
            pixmap.setMask(mask)
        icon_container.setIcon(QIcon(pixmap))
        return icon_container