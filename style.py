from PyQt5.QtGui import QLinearGradient

def background():
    return """
        QWidget {
            background: Qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgb(61, 217, 245), stop:1 rgb(240, 53, 218));
        }
    """

def main_page_box():
    return """
        QGroupBox {
            padding: 0;
            margin: 0;
            background-color: aqua;
        }
    """

def login_layout_box():
    return """
    QGroupBox {
        background-color: #fff;
        border: none;
        border-radius: 20px;
    }
    """

def title():
    return """
        QLabel {
            font-size: 25px;
            background-color: transparent;
            font: bold;
            font-family: Verdana, Tahoma, sans-serif;
            letter-spacing: 1.5px;
        }
        """

def login_feild():
    return """
    QGroupBox {
        background-color: #e5e5e5;
    }
    """

def login_submit_button():
    return """
    QPushButton {
        background-color: #1fcc44;
        color: white;
        font-size: 20px;
        border: none;
        border-radius: 20px;
    }
    """

def field_icon():
    return """
    QToolButton {
        background-color: transparent;
        color: #ddd;
    }
    """

def login_field():
    return """
    QLineEdit {
        background-color: transparent;
        color: #141414;
        border: none;
        font-size: 16px;

    }
    """

def bottom_label():
    return """
    QPushButton {
        background-color: transparent;
        border: none;
        outline: none;
    }
    """

def main_icon():
    return """
    QLabel {
         background-color: transparent;

    }
    """

def song_background():
    return """
    QLabel {
         border: 6px solid #1ED760;
         border-radius: 15px;
    }
    QPixmap {
        border-radius: 15px;
    }
    """

def sing_up_left():
    return """
    QGroupBox {
        background-color: #5ff4ee;
    }
    """
def sing_up_field():
    return """
    QGroupBox {
        background-color: transparent;
    }
    """


def singup_avatar():
    return """
    QLabel {
        background-color: transparent;
    }
    """

def home_page_background():
    return """
    QGroupBox{
        background: Qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgb(64,0,126), stop:1 rgb(0,255,160));
    }
    """

def home_page_top_box():
    return """
    QGroupBox{
        background: #fd367e;
    }
    """

def player_card_button():
    return """
    QPushButton {
        border-radius: 2px;
        background-color: #fd367e;
        font-size: 18px;
        border: 4px #a80038 solid; 
    }
    """

def player_card():
    return """
    QGroupBox {
        background-color: #eee;
        border-radius: 3px;
    }
    """

def player_background():
    return """
    QGroupBox {
        
    }
    """

def player_top_layout():
    return """
    QGroupBox {
        background-color: #15bb22;    
    }
    """

def player_bottom_layout():
    return """
    QGroupBox {
        background-color: #222;
    }
    """

def player_song_card():
    return """
    QGroupBox {
        border-image: none;
        border: none;
        border-radius: 15px;
        background-color: #222;
    }
    """

def music_player_song_title():
    return """
    QLabel {
        font-size: 20px;
        color: white;
        font-weight: 700;
    }
    """

def like_button():
    return """
    QPushButton {
        background-color: transparent;
    }
    QIcon {
        background-color: red;
    }
    """

def progress_bar():
    return """
    QProgressBar {
        border: solid grey;
        border-radius: 10px;
        color: black; }
    QProgressBar::chunk {
        background-color: #1ED760;
        border-radius :10px;
    }
    """

def volume_slider():
    return """
    QSlider {

    }
    """
def play_song_button():
    return """
    QPushButton {
        background-color: #1ED760;
        border: none;
        border-radius: 30px;
    }
    """

def continer():
    return """
    QGroupBox {
        background-color: #eee;
        border-top-left-radius: 10px;
        border-bottom-left-radius: 10px;
    }
    """

def container_label():
    return """
    QLabel {
        font-size: 18px;
    }
    """

def player_top_right():
    return """
    QGroupBox {
        border-image: none;
        border: none;
    }
    """


######### Playlist ########
def playlist_container():
    return """
    QGroupBox {
    }
    """

def playlist_label():
    return """
    QLabel {
        font-size: 16px;
    }
    """





####### Waiting Room - DJ #########
def waiting_main_layout_box():
    return """
    QGroupBox {

    }
    """


def waiting_users_grid_box():
    return """
    QGroupBox {
        
    }
    """

######## Party Room - DJ #######
def DJ_ctrl_section():
    return """
    QGroupBox {
        background-color: #222;
        border-radius: 10px;
    }
    """

def DJ_container():
    return """
    QGroupBox {

    }
    """

def DJ_users_title():
    return """
    QGroupBox {
        border: 2px solid black;
        font-size: 20px;
    }
    """


######## Chat #######
def chat_main():
    return """
    QGroupBox {
        background: qlineargradient(spread:pad, x1:0 y1:0, x2:0 y2:1, stop:0 #d6afff, stop:1 #687ED1)
    }
    """

def chat_left_side():
    return """
    QGroupBox {
        
    }
    """

def chat_right_side():
    return """
    QGroupBox {
        background-color: #E5DDD5;
        border-top-left-radius: 25px;
        border-bottom-left-radius: 25px;
    }
    """

def chat_profile_picture():
    return """
    QLabel {
        border: 2px solid white;
        border-radius : 30px; 
    }
    """

def chat_profile_name():
    return """
    QLabel {
        color: #fdfdfd;
        font-size: 18px;
        font-family: sans-serif;
    }
    """

def chat_top_right_layout():
    return """
    QGroupBox {
        background-color: #E5DDD5;
        margin: 12px;
        border-radius: 20px;
    }
    """

def chat_main_right_layout():
    return """
    QGroupBox {
        background-color: #E5DDD5;
        margin: 12px;
        border-radius: 20px;
    }
    """

def chat_main_right_scroll():
    return """
        QScrollArea {
        background-color: #E5DDD5;
    }
    """

def chat_main_scroll():
    return """
 QScrollBar:vertical
 {
     background-color: #2A2929;
     width: 20px;
     margin: 15px 3px 15px 3px;
     border: 1px transparent #2A2929;
     border-radius: 7px;
 }

 QScrollBar::handle:vertical
 {
     background-color: #d6afff;
     min-height: 5px;
     border-radius: 7px;
 }

 QScrollBar::sub-line:vertical
 {
     margin: 3px 0px 3px 0px;
     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);
     height: 10px;
     width: 10px;
     subcontrol-position: top;
     subcontrol-origin: margin;
 }

 QScrollBar::add-line:vertical
 {
     margin: 3px 0px 3px 0px;
     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);
     height: 10px;
     width: 10px;
     subcontrol-position: bottom;
     subcontrol-origin: margin;
 }

 QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on
 {

     border-image: url(:/qss_icons/rc/up_arrow.png);
     height: 10px;
     width: 10px;
     subcontrol-position: top;
     subcontrol-origin: margin;
 }


 QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
 {
     border-image: url(:/qss_icons/rc/down_arrow.png);
     height: 10px;
     width: 10px;
     subcontrol-position: bottom;
     subcontrol-origin: margin;
 }

 QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
 {
     background: none;
 }


 QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
 {
     background: none;
 }
"""
def chat_bottom_right_layout():
    return """
    QGroupBox {
        background-color: white;
        margin: 12px;
        border-radius: 20px;
    }
    """ 

def chat_room_title():
    return """
    QLabel {
        color: #d6afff;
        font-size: 24px;
        font-family: sans-serif;
        font-weight: 700;
    }
    """

def chat_message_input():
    return """
    QLineEdit {
        border: none;
        font-size: 20px;
        border-radius: 10px;
    }
    """

def chat_message_container_one():
    return """
    QGroupBox {
        background-color: white;
    }
    """

def chat_message_container_two():
    return """
        QGroupBox {
            background-color: #DCF8C6;
        }
    """

def empty():
    return """
    QGroupBox {
        background: transparent;
    }
    """




################## Playlist ##############3
def playlist_backgound():
    return """
    QGroupBox {
        background: #141414;
    }
    """

def playlist_title():
    return """
    QLabel {
        color: white;
        font-size: 22px;
        font-weight: 700;
    }
    """

def playlist_window_label():
    return """
    QLabel {
        color: white;
        font-size: 16px;
    }
    """

def playlist_id():
    return """
    QLabel {
        color: white;
        border: 1px solid black;
        font-size: 22px;
        border-radius: 14px;
    }
    """

