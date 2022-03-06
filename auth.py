import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QIcon, QPixmap
import random
import style
from Database import database
from spotifyClient import spotifyAPI


class Auth(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 550)
        self.setWindowTitle("Music App")
        self.setStyleSheet(style.background())
        self.database = database()
        self.database.print_all_database()
        self.database.print_all_songs()
        self.UI()

    #################### Main Window UI #####################

    def UI(self):
        self.main_page = QHBoxLayout()
        self.main_page_box = QGroupBox('main page box')
        self.main_page_box.setObjectName('main_page_box')
        self.main_page_box.setStyleSheet(style.main_page_box())
        self.main_page_box.setAlignment(Qt.AlignCenter)
        self.main_page_box.setLayout(self.main_page)

        self.page_system = QStackedWidget()

        self.login_page()
        self.sing_up_page()

        self.page_system.addWidget(self.login_layout_box)
        self.page_system.addWidget(self.singup_layout_box)

        self.main_page.addWidget(self.page_system, alignment=Qt.AlignCenter)
        self.setLayout(self.main_page)
        self.show()
    #################### Main Window UI #####################

    #################### Dealing With Multiple Pages #####################

    def insert_page(self, widget, index=-1):
        self.page_system.insertWidget(index, widget)

    def go_to_page(self, number):
        self.page_system.setCurrentIndex(number)
    #################### Dealing With Multiple Pages #####################

    #################### Database Stuff #####################
    def authenticate_db(self):
        username = self.user_field.text()
        password = self.password_field.text()
        code = self.database.authenticate(username, password)

    def create_user_db(self):
        ### Getting the values from the felds in the sing up page ###
        username = self.singup_username_line_edit.text()
        email = self.singup_email_line_edit.text()
        password = self.singup_password_line_edit.text()
        prepassword = self.singup_prepasswprd_line_edit.text()
        code = self.database.create_user(
            username, email, password, prepassword)
        self.make_message_box(code)
    #################### Database Stuff #####################

    #################### Logistic Functions #####################

    def make_message_box(self, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.setFixedSize(100, 100)
        msg.exec_()

    def clear_auth_fields(self):
        # Clear the fields of the singup and login #
        self.singup_username_line_edit.setText('')
        self.singup_email_line_edit.setText('')
        self.singup_password_line_edit.setText('')
        self.singup_prepasswprd_line_edit .setText('')

        self.user_field.setText('')
        self.password_field.setText('')
    #################### Logistic Functions #####################

    #################### Sing Up Page #####################

    def make_singup_avatar(self):
        number = random.randint(1, 4)
        label = QLabel()
        label.setPixmap(QPixmap(f'undraw-{number}.svg'))
        label.setStyleSheet(style.singup_avatar())
        return label

    def make_singup_mini_profile(self):
        profile = QLabel('Profile')
        profile.setPixmap(QPixmap('headphone_image.png'))
        profile.setAlignment(Qt.AlignHCenter)
        profile.setFixedSize(100, 100)
        return profile

    def sing_up_page(self):
        self.sing_up_Widgets()
        self.sing_up_layouts()

    def sing_up_Widgets(self):
        ### Right Side Widget ###
        self.sing_up_title = QLabel('Create New User')
        self.sing_up_title.setAlignment(Qt.AlignHCenter)
        self.sing_up_title.setStyleSheet(style.title())

        self.sing_up_username_field = QHBoxLayout()
        self.sing_up_username_field_box = QGroupBox()
        self.sing_up_username_field_box.setStyleSheet(style.login_feild())
        self.sing_up_username_field_box.setFixedSize(300, 40)
        self.sing_up_username_field_box.setLayout(self.sing_up_username_field)

        self.sing_up_email_field = QHBoxLayout()
        self.sing_up_email_field_box = QGroupBox()
        self.sing_up_email_field_box.setStyleSheet(style.login_feild())
        self.sing_up_email_field_box.setFixedSize(300, 40)
        self.sing_up_email_field_box.setLayout(self.sing_up_email_field)

        self.sing_up_password_field = QHBoxLayout()
        self.sing_up_password_field_box = QGroupBox()
        self.sing_up_password_field_box.setStyleSheet(style.login_feild())
        self.sing_up_password_field_box.setFixedSize(300, 40)
        self.sing_up_password_field_box.setLayout(self.sing_up_password_field)

        self.sing_up_pre_password_field = QHBoxLayout()
        self.sing_up_pre_password_field_box = QGroupBox()
        self.sing_up_pre_password_field_box.setStyleSheet(style.login_feild())
        self.sing_up_pre_password_field_box.setFixedSize(300, 40)
        self.sing_up_pre_password_field_box.setLayout(
            self.sing_up_pre_password_field)

        self.sing_up_authentication = QPushButton('Sing Up')
        self.sing_up_authentication.setCursor(Qt.PointingHandCursor)
        self.sing_up_authentication.setFixedSize(300, 40)
        self.sing_up_authentication.clicked.connect(self.create_user_db)
        self.sing_up_authentication.setStyleSheet(style.login_submit_button())

        self.sing_up_return_button = QPushButton(
            'Already have a user? go to login')
        self.sing_up_return_button.setCursor(Qt.PointingHandCursor)
        self.sing_up_return_button.setStyleSheet(style.bottom_label())
        self.sing_up_return_button.clicked.connect(lambda: self.go_to_page(0))

        ### Sing Up Fields Widgets ###
        self.singup_username_line_edit = QLineEdit()
        self.singup_username_line_edit.setPlaceholderText('Username')
        self.singup_username_line_edit.setStyleSheet(style.login_field())
        self.singup_username_icon = QToolButton()
        self.singup_username_icon.setStyleSheet(style.field_icon())
        self.singup_username_icon.setDisabled(True)
        self.singup_username_icon.setIcon(QIcon('user-solid.svg'))

        self.singup_email_line_edit = QLineEdit()
        self.singup_email_line_edit.setPlaceholderText('Email')
        self.singup_email_line_edit.setStyleSheet(style.login_field())
        self.singup_email_icon = QToolButton()
        self.singup_email_icon.setStyleSheet(style.field_icon())
        self.singup_email_icon.setDisabled(True)
        self.singup_email_icon.setIcon(QIcon('user-solid.svg'))

        self.singup_password_line_edit = QLineEdit()
        self.singup_password_line_edit.setPlaceholderText('password')
        self.singup_password_line_edit.setEchoMode(QLineEdit.Password)
        self.singup_password_line_edit.setStyleSheet(style.login_field())
        self.singup_password_icon = QToolButton()
        self.singup_password_icon.setStyleSheet(style.field_icon())
        self.singup_password_icon.setDisabled(True)
        self.singup_password_icon.setIcon(QIcon('lock-solid.svg'))

        self.singup_prepasswprd_line_edit = QLineEdit()
        self.singup_prepasswprd_line_edit.setPlaceholderText(
            'Validate Password')
        self.singup_prepasswprd_line_edit.setStyleSheet(style.login_field())
        self.singup_prepasswprd_line_edit.setEchoMode(QLineEdit.Password)
        self.singup_prepasswprd_icon = QToolButton()
        self.singup_prepasswprd_icon.setStyleSheet(style.field_icon())
        self.singup_prepasswprd_icon.setDisabled(True)
        self.singup_prepasswprd_icon.setIcon(QIcon('lock-solid.svg'))

        ### Left Side Widgets ###
        self.singup_avatar = self.make_singup_avatar()

    def sing_up_layouts(self):
        ##### Sing Up Layouts #####
        self.singup_layout = QHBoxLayout()
        self.singup_layout.setAlignment(Qt.AlignCenter)

        self.singup_layout_box = QGroupBox()
        self.singup_layout_box.setStyleSheet(style.login_layout_box())
        self.singup_layout_box.setFixedSize(650, 450)
        self.singup_layout_box.setLayout(self.singup_layout)

        self.sing_up_left = QVBoxLayout()
        self.sing_up_right = QVBoxLayout()

        ### Create The Right Part ###
        self.sing_up_title_section = QVBoxLayout()
        self.sing_up_form_section = QVBoxLayout()
        self.sing_up_bottom_section = QVBoxLayout()

        ### Create The Left Part ###
        self.sing_up_left.addWidget(self.singup_avatar)

        ### Create The Fields ###

        ### Adding the nested Layouts ###
        self.main_page.addWidget(self.singup_layout_box)

        self.singup_layout.addLayout(self.sing_up_left, 50)
        self.singup_layout.addLayout(self.sing_up_right, 50)

        self.sing_up_right.addLayout(self.sing_up_title_section, 20)
        self.sing_up_right.addLayout(self.sing_up_form_section, 60)
        self.sing_up_right.addLayout(self.sing_up_bottom_section, 20)

        # Right Part #
        self.sing_up_title_section.addStretch()
        self.sing_up_title_section.addWidget(self.sing_up_title)
        self.sing_up_title_section.addStretch()

        self.sing_up_form_section.addStretch()
        self.sing_up_form_section.addWidget(self.sing_up_username_field_box)
        self.sing_up_form_section.addStretch()
        self.sing_up_form_section.addWidget(self.sing_up_email_field_box)
        self.sing_up_form_section.addStretch()
        self.sing_up_form_section.addWidget(self.sing_up_password_field_box)
        self.sing_up_form_section.addStretch()
        self.sing_up_form_section.addWidget(
            self.sing_up_pre_password_field_box)
        self.sing_up_form_section.addStretch()
        self.sing_up_form_section.addWidget(self.sing_up_authentication)
        self.sing_up_right.addStretch()

        self.sing_up_bottom_section.addStretch()
        self.sing_up_bottom_section.addWidget(self.sing_up_return_button)
        self.sing_up_bottom_section.addStretch()

        self.sing_up_username_field.addWidget(self.singup_username_icon)
        self.sing_up_username_field.addWidget(self.singup_username_line_edit)

        self.sing_up_email_field.addWidget(self.singup_email_icon)
        self.sing_up_email_field.addWidget(self.singup_email_line_edit)

        self.sing_up_password_field.addWidget(self.singup_password_icon)
        self.sing_up_password_field.addWidget(self.singup_password_line_edit)

        self.sing_up_pre_password_field.addWidget(self.singup_prepasswprd_icon)
        self.sing_up_pre_password_field.addWidget(
            self.singup_prepasswprd_line_edit)

    #################### Sing Up Page #####################

    #################### Login Page #####################

    def login_page(self):
        self.login_Widgets()
        self.login_layouts()
        self.login_layout.setGeometry(QRect(150, 100, 800, 550))

    def login_layouts(self):
        ##### Create The Layouts #####
        ### Login Layouts ###
        self.login_layout = QHBoxLayout()

        self.login_layout_box = QGroupBox()
        self.login_layout_box.setStyleSheet(style.login_layout_box())
        self.login_layout_box.setFixedSize(650, 450)
        self.login_layout_box.setLayout(self.login_layout)

        self.login_right_layout = QVBoxLayout()
        self.login_left_layout = QVBoxLayout()

        ### Create the right part ###
        self.title_section = QHBoxLayout()
        self.form_section = QVBoxLayout()
        self.bottom_section = QVBoxLayout()

        ### Create The Form ###
        self.username_layout = QHBoxLayout()
        self.username_layout.addWidget(self.user_icon)
        self.username_layout.addWidget(self.user_field)
        self.username_layout_box = QGroupBox()
        self.username_layout_box.setLayout(self.username_layout)
        self.username_layout_box.setAlignment(Qt.AlignHCenter)
        self.username_layout_box.setFixedSize(300, 40)
        self.username_layout_box.setStyleSheet(style.login_feild())

        self.password_layout = QHBoxLayout()
        self.password_layout.addWidget(self.password_icon)
        self.password_layout.addWidget(self.password_field)
        self.password_layout_box = QGroupBox()
        self.password_layout_box.setLayout(self.password_layout)
        self.password_layout_box.setAlignment(Qt.AlignHCenter)
        self.password_layout_box.setFixedSize(300, 40)
        self.password_layout_box.setStyleSheet(style.login_feild())

        ### Create the right part ###
        self.login_right_layout.addWidget(self.logo)

        ### Adding the nesting layouts ###
        # self.main_page.addWidget(self.login_layout_box)

        self.login_layout.addLayout(self.login_right_layout, 50)
        self.login_layout.addLayout(self.login_left_layout, 50)

        self.login_left_layout.addLayout(self.title_section, 20)
        self.login_left_layout.addLayout(self.form_section, 55)
        self.login_left_layout.addLayout(self.bottom_section, 25)

        self.form_section.addStretch()
        self.title_section.addWidget(self.title)
        self.form_section.addWidget(self.username_layout_box)
        self.form_section.addStretch()
        self.form_section.addWidget(self.password_layout_box)
        self.form_section.addStretch()
        self.form_section.addWidget(self.login_submit_button)
        self.form_section.addStretch()

        # self.bottom_section.addStretch()
        self.bottom_section.addWidget(self.forgot_password_label)
        self.bottom_section.addStretch()
        self.bottom_section.addWidget(self.create_user_label)
        self.bottom_section.addStretch()

    def login_Widgets(self):
        ##### Making the widgets for the app #####
        # self.main_page = QHBoxLayout()
        # self.main_page_box = QGroupBox('main page box')
        # self.main_page_box.setObjectName('main_page_box')
        # self.main_page_box.setStyleSheet(style.main_page_box())
        # self.main_page_box.setLayout(self.main_page)

        ### Title Section ###
        self.title = QLabel('Member Login')
        self.title.setStyleSheet(style.title())
        self.title.setAlignment(Qt.AlignCenter)

        ### Login Button ###
        self.login_submit_button = QPushButton('Login')
        self.login_submit_button.setFixedSize(300, 40)
        self.login_submit_button.setCursor(Qt.PointingHandCursor)
        self.login_submit_button.setStyleSheet(style.login_submit_button())
        self.login_submit_button.clicked.connect(self.authenticate_db)

        ### Field Widgets ###
        self.user_icon = QToolButton()
        self.user_icon.setDisabled(True)
        self.user_icon.setStyleSheet(style.field_icon())
        self.user_icon.setIcon(QIcon("user-solid.svg"))
        self.user_field = QLineEdit()
        self.user_field.setFrame(False)
        self.user_field.setPlaceholderText('Username')
        self.user_field.setStyleSheet(style.login_field())

        self.password_icon = QToolButton()
        self.password_icon.setDisabled(True)
        self.password_icon.setStyleSheet(style.field_icon())
        self.password_icon.setIcon(QIcon("lock-solid.svg"))
        self.password_field = QLineEdit()
        self.password_field.setFrame(False)
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setPlaceholderText('Password')
        self.password_field.setStyleSheet(style.login_field())

        ### Bottom Widgets ###
        self.forgot_password_label = QPushButton('Forgot Password ?')
        self.forgot_password_label.setStyleSheet(style.bottom_label())
        self.forgot_password_label.setCursor(Qt.PointingHandCursor)

        self.create_user_label = QPushButton('Create new account =>')
        self.create_user_label.setStyleSheet(style.bottom_label())
        self.create_user_label.setCursor(Qt.PointingHandCursor)
        self.create_user_label.clicked.connect(lambda: self.go_to_page(1))
        self.create_user_label.clicked.connect(self.clear_auth_fields)
        # self.create_user_label.mouseReleaseEvent = self.go_to_singup

        ### Left Part ###
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap('logo.svg'))
        self.logo.setStyleSheet(style.main_icon())
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setFixedSize(250, 250)
    #################### Login Page #####################
