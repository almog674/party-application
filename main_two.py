import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTime, QTimer, QSize, QThread, pyqtSignal, QMargins, QEvent
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QImage, QColor, QLinearGradient
import socket
import cv2
from gui_helper import Gui_Helper
if __name__ == '__main__':
    from labrary_base import *
    from music_player import Music_Player
    from playlist_window import playlist_window
    from auth import Auth
    from dj import DJ
    from user import User
    from Person import Person


class Main(QWidget):
    def __init__(self, username, execute=True):
        super().__init__()
        self.username = username
        self.database = database()
        self.spotiy_client = spotifyAPI(
            client_id='9c8a8a4cfe9c492a86eced46e6ac829b', client_secret='6d71b04b746c4ca6bb548f79a13bfb26')
        self.client = self.initialize_client()
        self.music_player_page = Music_Player(self.username, self)

    #################### Main Window UI #####################
    def UI(self):
        self.main_page = QHBoxLayout()

        self.home_page()

        self.page_system = QStackedWidget()

        self.page_system.addWidget(self.home_page_box)

        self.music_player_page.setGeometry(150, 100, 950, 675)
        self.music_player_page.UI()
        self.page_system.addWidget(self.music_player_page)

        self.main_page.addWidget(self.page_system)
        self.setLayout(self.main_page)
        self.show()

    #################### Main Window UI #####################

    #################### Sockets and Networking #####################
    def initialize_client(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return client
    #################### Sockets and Networking #####################

    #################### Logistic Functions #####################
    def make_timer_label(self):
        current_time = QTime.currentTime()
        label_string = current_time.toString('hh:mm:ss')
        self.timer_label_homepage.setText(label_string)

    @staticmethod
    def get_current_time():
        time_now = time.strftime('%H:%M', time.gmtime())
        return time_now

    #################### Logistic Functions #####################

    #################### Dealing With Multiple Pages #####################

    def insert_page(self, widget, index=-1):
        self.page_system.insertWidget(index, widget)

    def go_to_page(self, index):
        self.page_system.setCurrentIndex(index)

    #################### Dealing With Multiple Pages #####################

    #################### Spotify Client #####################

    #################### Spotify Client #####################

    #################### Home Page #####################

    def home_page(self):
        self.home_page_widgets()
        self.home_page_layouts()

    def home_page_widgets(self):
        self.name_label = QLabel(self.username)
        self.timer_label_homepage = QLabel()
        self.timer_clock = QTimer()
        self.timer_clock.timeout.connect(self.make_timer_label)
        self.timer_clock.start(1000)
        self.make_timer_label()

        ### Player card ###
        self.player_card_image = QLabel()
        self.player_card_image_pixmap = QPixmap('player-picture.svg')
        self.player_card_image_pixmap = self.player_card_image_pixmap.scaled(
            200, 300, Qt.KeepAspectRatio)
        self.player_card_image.setPixmap(self.player_card_image_pixmap)

        self.player_card_title = QPushButton('Song Player')
        self.player_card_title.setFixedHeight(40)
        self.player_card_title.setCursor(Qt.PointingHandCursor)
        self.player_card_title.clicked.connect(lambda: self.go_to_page(1))
        self.player_card_title.setStyleSheet(style.player_card_button())

        ### Join Party card ###
        self.join_party_card_image = QLabel()
        self.join_party_card_image_pixmap = QPixmap('party-picture.svg')
        self.join_party_card_image_pixmap = self.join_party_card_image_pixmap.scaled(
            200, 300, Qt.KeepAspectRatio)
        self.join_party_card_image.setPixmap(self.join_party_card_image_pixmap)

        self.join_party_card_title = QPushButton('Join Party')
        self.join_party_card_title.setFixedHeight(40)
        self.join_party_card_title.setCursor(Qt.PointingHandCursor)
        self.join_party_card_title.setStyleSheet(style.player_card_button())

        ### Open Party card ###
        self.open_party_card_image = QLabel()
        self.open_party_card_image_pixmap = QPixmap('dj-picture.svg')
        self.open_party_card_image_pixmap = self.open_party_card_image_pixmap.scaled(
            200, 300, Qt.KeepAspectRatio)
        self.open_party_card_image.setPixmap(self.open_party_card_image_pixmap)

        self.open_party_card_title = QPushButton('Open Party')
        self.open_party_card_title.setFixedHeight(40)
        self.open_party_card_title.setCursor(Qt.PointingHandCursor)
        self.open_party_card_title.setStyleSheet(style.player_card_button())

    def home_page_layouts(self):
        self.home_page_layout = QVBoxLayout()
        self.home_page_box = QGroupBox()
        self.home_page_box.setStyleSheet(style.home_page_background())
        self.home_page_box.setLayout(self.home_page_layout)

        self.home_page_top = QHBoxLayout()
        self.home_page_top_box = QGroupBox()
        self.home_page_top_box.setFixedHeight(40)
        self.home_page_top_box.setStyleSheet(style.home_page_top_box())
        self.home_page_top_box.setLayout(self.home_page_top)
        self.home_page_bottom = QHBoxLayout()

        ### Build the top ###
        self.home_page_top.addWidget(self.name_label)
        self.home_page_top.addStretch()
        self.home_page_top.addWidget(self.timer_label_homepage)

        ### Build the bottom ###
        self.player_card = QVBoxLayout()
        self.player_card_box = QGroupBox()
        self.player_card_box.setStyleSheet(style.player_card())
        self.player_card_box.setFixedSize(200, 300)
        self.player_card_box.setLayout(self.player_card)

        self.join_party_card = QVBoxLayout()
        self.join_party_card_box = QGroupBox()
        self.join_party_card_box.setStyleSheet(style.player_card())
        self.join_party_card_box.setFixedSize(200, 300)
        self.join_party_card_box.setLayout(self.join_party_card)

        self.open_party_card = QVBoxLayout()
        self.open_party_card_box = QGroupBox()
        self.open_party_card_box.setStyleSheet(style.player_card())
        self.open_party_card_box.setFixedSize(200, 300)
        self.open_party_card_box.setLayout(self.open_party_card)

        # Adding the nested layouts
        self.home_page_layout.addWidget(self.home_page_top_box, 10)
        self.home_page_layout.addStretch(3)
        self.home_page_layout.addLayout(self.home_page_bottom, 90)
        self.home_page_layout.addStretch(1)

        self.home_page_bottom.addWidget(self.player_card_box)
        self.home_page_bottom.addWidget(self.join_party_card_box)
        self.home_page_bottom.addWidget(self.open_party_card_box)

        self.player_card.addStretch()
        self.player_card.addWidget(self.player_card_image)
        self.player_card.addStretch()
        self.player_card.addWidget(self.player_card_title)
        self.player_card.addStretch()

        self.join_party_card.addStretch()
        self.join_party_card.addWidget(self.join_party_card_image)
        self.join_party_card.addStretch()
        self.join_party_card.addWidget(self.join_party_card_title)
        self.join_party_card.addStretch()

        self.open_party_card.addStretch()
        self.open_party_card.addWidget(self.open_party_card_image)
        self.open_party_card.addStretch()
        self.open_party_card.addWidget(self.open_party_card_title)
        self.open_party_card.addStretch()

    #################### Home Page #####################


def main():
    App = QApplication(sys.argv)
    auth_window = Auth()
    main_window = Main('almog999')
    main_window.UI()
    main_window.setGeometry(150, 100, 950, 675)
    main_window.setWindowTitle("Music App")
    dj = DJ('almog999')
    user = User('roee90')
    user2 = User('pokemon go')
    time.sleep(1)
    user2.UI()
    dj.UI()
    user.UI()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
