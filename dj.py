from main_two import Main
from labrary_base import *
from Person import Person
from room import Room
import math
from chat import Chat_Data, Chat_UI
import threading
from gui_threads import Gui_Thread_DJ


class DJ(QWidget, Person):
    def __init__(self, name):
        QWidget.__init__(self, name = name)
        self.active = False
        self.playlist_now = []
        self.chat = None

        self.gui_thread = Gui_Thread_DJ()
        self.database_tool.print_all_songs()

        self.initialize_room()
        self.latest_data_thread = threading.Thread(target = self.check_latest_data)
        self.chat_data_thread = threading.Thread(target = self.check_chat_data)
        self.playlist_thread = threading.Thread(target = self.check_playlist)
        self.playlist_thread.start()
        
    ######################### Room Functions ################################
    def initialize_room(self):
        self.send_message_to_server(self.name, 10, None)

    def change_room_code(self):
        self.send_message_to_server(self.name, 12, None)
        self.update_waiting_page()

    def change_room_title(self):
        text, okpressed = QInputDialog.getText(self, 'Choose new name', 'Name: ')
        if okpressed and text != '':
            self.send_message_to_server(self.name, 13, text)
        self.update_waiting_page()

    ######################### Room Functions ################################


    ######################### Chat Functions ################################
    def open_chat(self):
        if not self.chat:
            self.chat = self.room.chat
            self.chat_ui = Chat_UI(self.chat, self)
            self.chat_ui.show()
            self.chat_data_thread.start()
            time.sleep(0.1)
            self.chat_ui.build_message_text()
        else:
            self.chat_ui.show()

    def send_message(self):
        message_text = self.chat_ui.message_input.text()
        message = {
                    'message_name' : self.name,
                    'message_text' : message_text,
                    'message_date' : self.get_current_time()
                  }
        self.send_message_to_server(self.name, 31, message)

    def update_chat(self):
        if self.chat:
            self.chat_ui.update_chat_data(self.chat)
            self.chat_ui.build_message_text()

    def check_chat_data(self):
        while True:
            if len(self.socket_client.new_messages) > 0:
                data = self.socket_client.new_messages[0]
                self.socket_client.new_messages.remove(data)
                self.chat = data
                self.update_chat()
            else:
                time.sleep(0.1)
    ######################### Chat Functions ################################

    ######################### Logistic Functions ################################
    def play_song(self):
        self.music_player.play_song_not_locally(self.DJ_play_button, self.DJ_progress_bar, self.timer, self.DJ_song_name)
        self.send_message_to_server(self.name, 21, self.music_player.song_index)
        self.music_player.update_play_button(self.DJ_play_button)

    def play_next(self):
        self.music_player.change_song(1, lambda: self.music_player.play_song_not_locally(self.DJ_play_button, self.DJ_progress_bar, self.timer, self.DJ_song_name))

    def play_previous(self):
        self.music_player.change_song(-1, lambda: self.music_player.play_song_not_locally(self.DJ_play_button, self.DJ_progress_bar, self.timer, self.DJ_song_name))

    def update_waiting_page(self):
        self.waiting_title.setText(self.room.name)
        if threading.main_thread() == threading.current_thread():
            self.build_waiting_users_grid()
        else:
            time.sleep(0.05)
            self.gui_thread.update_waiting_page.connect(self.update_waiting_page)
            time.sleep(0.1)
            self.gui_thread.update_waiting_page_func()
        self.waiting_code.setText(self.room.code)

    def update_DJ_page(self):
        if self.music_player.current_song:
            self.DJ_song_name.setText(self.music_player.current_song['song_name'])

        if threading.main_thread() == threading.current_thread():
            self.update_DJ_users_list()
        else:
            time.sleep(0.05)
            self.gui_thread.update_party_page.connect(self.update_DJ_page)
            time.sleep(0.1)
            self.gui_thread.update_party_page_func()

    def kick_user(self, user, button):
        self.send_message_to_server(self.name, 5, None, receiver = user)

    def make_popup(self, text):
        popup = QHBoxLayout(self)
        popup.setFixedSize(100, 100)

        popup_text = QLabel(text)
        popup_text.setStyleSheet(style.container_label())

        popup.addWidget(popup_text)

    def go_to_page(self, value):
        page_number, page_geometry, page_title = value
        first, second, third, fourth = page_geometry
        self.page_system.setCurrentIndex(page_number)
        self.setGeometry(first, second, third, fourth)
        self.setWindowTitle(page_title)

    def go_to_waiting_page(self):
        self.gui_thread.room_value.connect(self.go_to_page)
        self.gui_thread.go_to_page_0()
        

    def go_to_dj_page(self):
        self.gui_thread.room_value.connect(self.go_to_page)
        self.gui_thread.go_to_page_1()
        
    def start_party(self):
        self.active = True
        self.go_to_dj_page()
        self.send_message_to_server(self.name, 11,  text = None)

    def make_play_list(self):
        playlist = []
        for song in self.music_player.play_list_now:
            playlist.append(song['song_name'])
        return playlist

    def update_playlist(self):
        message_text = self.make_play_list()
        self.send_message_to_server(self.name, 20, text = str(message_text))
        self.playlist_now.clear()
        for item in self.music_player.play_list_now:
            self.playlist_now.append(item)


    def check_playlist(self):
        while True:
            if self.playlist_now != self.music_player.play_list_now:
                self.update_playlist()
            time.sleep(2)
        print('finished')

    def add_song_func(self, event):
        self.music_player.open_search_song_window(None)

    def playlist_func(self, event):
        self.music_player.open_playlist_window(None)

    def end_party_func(self, event):
        self.send_message_to_server(self.name, 15, None)
        self.kicked = True
        self.closeEvent(event)

    def add_local_song_func(self, event):
        self.music_player.open_add_song_window(None)

    def closeEvent(self, event):
        if self.kicked == False:
            self.send_message_to_server(self.name, 15, None)
            self.send_message_to_server(self.name, 4, None)
        try:
            self.music_player.music_player.music.unload()
        except Exception as e:
            print(e)
        self.kicked = True
        self.close()

    def ask_for_opinion(self):
        self.send_message_to_server(self.name, 16, None)

    ######################### Logistic Functions ################################
    def check_latest_data(self):
        while True:
            if len(self.socket_client.latest_data) > 0:
                data = self.socket_client.latest_data[0]
                self.socket_client.latest_data.remove(data)
                self.latest_data_functionality(data)
            else:
                time.sleep(0.1)   


    def latest_data_functionality(self, latest_data):
        if isinstance(latest_data, Room):
            self.room = latest_data
            if self.active == False:
                self.update_waiting_page()
            elif self.active == True:
                self.update_DJ_page()
                self.update_chat()
        elif isinstance(latest_data, dict):
            if latest_data['message_type']:
                if latest_data['message_type'] == 'popup':
                    self.make_popup(latest_data['message'])
                elif latest_data['message_type'] == 'error':
                    self.make_message_box(latest_data['message'])
        else:
            print(latest_data)

    ######################### Special Widgets ################################
    def build_waiting_users_grid(self):
        counter = 0
        self.gui_thread.delete_waiting_user_grid.connect(lambda: self.clear_layout(self.waiting_users_grid))
        self.gui_thread.delete_waiting_grid()
        for user in self.room.users:
            container = self.build_waiting_users_single(user, counter)
            counter += 1
            self.waiting_users_grid.addLayout(container, counter, math.floor(counter / 5))

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            self.delete_item_from_layout(layout.itemAt(i))

    def delete_item_from_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.delete_item_from_layout(item.layout())

    def build_waiting_users_single(self, user, counter):
        container = QHBoxLayout()
        title = QLabel(user)
        button = QPushButton(f'Del #{counter}')
        button.clicked.connect(lambda: self.kick_user(user, button))

        container.addWidget(title)
        container.addWidget(button)
        return container


    ######################### Special Widgets ################################        

    
    ######################### UI ################################
    def UI(self):
        self.main_page = QHBoxLayout()

        self.setGeometry(150, 100, 950, 675)
        self.setWindowTitle("DJ Party")

        self.page_system = QStackedWidget()

        self.waiting_room()
        self.DJ_room()

        self.page_system.addWidget(self.waiting_main_layout_box)
        self.page_system.addWidget(self.DJ_main_layout_box)

        self.main_page.addWidget(self.page_system)
        self.setLayout(self.main_page)
        self.latest_data_thread.start()
        self.show()
    

    def waiting_room(self):
        self.waiting_room_widgets()
        self.waiting_room_layouts()
        

    def waiting_room_layouts(self):
        self.waiting_main_layout = QVBoxLayout()
        self.waiting_main_layout_box = QGroupBox()
        self.waiting_main_layout_box.setStyleSheet(style.waiting_main_layout_box())
        self.waiting_main_layout_box.setLayout(self.waiting_main_layout)

        self.waiting_title_layout = QHBoxLayout()

        self.waiting_code_layout = QHBoxLayout()

        self.waiting_users_grid = QGridLayout()
        self.waiting_users_grid_box = QGroupBox()
        self.waiting_users_grid_box.setStyleSheet(style.waiting_users_grid_box())
        self.waiting_users_grid_box.setLayout(self.waiting_users_grid)


        ############## Adding the Widgets to the layouts #############

        self.waiting_title_layout.addWidget(self.waiting_title)
        self.waiting_title_layout.addWidget(self.waiting_title_edit)

        self.waiting_code_layout.addWidget(self.waiting_code)
        self.waiting_code_layout.addWidget(self.waiting_code_edit)

        self.waiting_main_layout.addLayout(self.waiting_title_layout)
        self.waiting_main_layout.addLayout(self.waiting_code_layout)
        self.waiting_main_layout.addWidget(self.waiting_users_grid_box)
        self.waiting_main_layout.addWidget(self.waiting_start_button)

        

    def waiting_room_widgets(self):
        # self.waiting_title = QLabel(self.room.name)
        self.waiting_title = QLabel('Regular Room')
        self.waiting_title_edit = QPushButton('Edit Title')
        self.waiting_title_edit.clicked.connect(self.change_room_title)

        # self.waiting_code = QLabel(self.room.code)
        self.waiting_code = QLabel('00000000')
        self.waiting_code_edit = QPushButton('Edit Code')
        self.waiting_code_edit.clicked.connect(self.change_room_code)

        self.waiting_start_button = QPushButton('Start The Party!')
        self.waiting_start_button.clicked.connect(self.start_party)

    ######################### UI ################################


    ######################### DJ Room Special Widgets ################################
    def make_container(self, text, icon, function):
        container = QHBoxLayout()
        container_box = QGroupBox()
        container_box.setStyleSheet(style.DJ_container())
        container_box.setCursor(Qt.PointingHandCursor)
        container_box.setLayout(container)

        container_text = QLabel(text)
        container_text.setStyleSheet(style.container_label())

        container_icon = QPushButton()
        container_icon.setIcon(QIcon(icon))
        container_icon.setIconSize(QSize(30, 30))
        container_icon.setStyleSheet(style.like_button())

        container_box.mouseReleaseEvent = function
        container_text.mouseReleaseEvent = function
        container_icon.mouseReleaseEvent = function

        container.addWidget(container_text)
        container.addWidget(container_icon)
        return container, container_box

    def make_users_label(self):
        label = QLabel('Users List')
        label.setFixedHeight(50)
        label.setStyleSheet(style.DJ_users_title())
        label.setToolTip('This is all the users in the Party')
        return label

    def make_user_single(self, name, like = False, hate = False):
        container = QHBoxLayout()
        container_icon = QLabel()
        user_picture = QPixmap('user-solid.svg')
        user_picture = user_picture.scaled(30, 30, Qt.KeepAspectRatio)
        container_icon.setPixmap(user_picture)
        container_name = QLabel(name)
        if like == True:
            icon_url = 'player_icons\heart-full-icon.svg'
        elif hate == True:
            icon_url = 'player_icons\pause-icon.svg'
        else:
            icon_url = 'player_icons\heart-icon.svg'
        container_like_icon = self.music_player.make_button(icon_url, 30, 30, color = 'red')
        container_kick_button = self.music_player.make_button('player_icons\\trash-icon.svg', 30, 30, color = 'black')

        container.addWidget(container_icon)
        container.addWidget(container_name)
        container.addWidget(container_like_icon)
        container.addWidget(container_kick_button)
        return container

    def make_DJ_users_list(self):
        like = False
        hate = False
        self.DJ_users_list = QGridLayout()
        if self.room:
            self.gui_thread.delete_DJ_users_list.connect(lambda: self.clear_layout(self.DJ_users_list))
            self.gui_thread.delete_DJ_users_list_func()
            for index, user in enumerate(self.room.users):
                if user in self.room.like_users:
                    like = True
                if user in self.room.hate_users:
                    hate = True
                user_container = self.make_user_single(user, like = like, hate = hate)
                self.DJ_users_list.addLayout(user_container, index, 0)
            self.DJ_main_right_layout.addWidget(self.DJ_users_title)
            self.DJ_main_right_layout.addLayout(self.DJ_users_list)

    def update_DJ_users_list(self):
        like = False
        hate = False
        self.gui_thread.delete_DJ_users_list.connect(lambda: self.clear_layout(self.DJ_users_list))
        self.gui_thread.delete_DJ_users_list_func()
        for index, user in enumerate(self.room.users):
                if user in self.room.like_users:
                    like = True
                if user in self.room.hate_users:
                    hate = True
                user_container = self.make_user_single(user, like = like, hate = hate)
                self.DJ_users_list.addLayout(user_container, index, 0)

    def handle_changed_value(self):
        self.music_player.update_volume_icon(self.DJ_volium_slide, self.DJ_volium_icon)
        self.music_player.music_player.music.set_volume(self.DJ_volium_slide.value() / 100)

    ######################### DJ Room Special Widgets ################################




    ######################### DJ Room UI ################################

    def DJ_room(self):
        self.DJ_room_widgets()
        self.DJ_room_layouts()

    def DJ_room_widgets(self):
        ###### Right Part #####
        ### Top Section ###
        self.DJ_chat_button = QPushButton('Open Chat')
        self.DJ_chat_button.clicked.connect(self.open_chat)

        ### Song Section ###
        self.DJ_song_name = QLabel('Nothing yet...')
        self.DJ_progress_bar = self.music_player.make_progress_bar()

        ### Ctrl Section ###
        self.DJ_like_button = self.music_player.make_button('player_icons\heart-full-icon.svg', 35, 35, color = None)
        self.DJ_like_button.clicked.connect(self.ask_for_opinion)
        self.DJ_previous_button = self.music_player.make_button('player_icons\previous-song-icon.svg', 35, 35, color = None)
        self.DJ_previous_button.clicked.connect(self.play_previous)
        self.DJ_play_button = self.music_player.make_button('player_icons\play-icon.svg', 35, 35, color = None)
        self.DJ_play_button.clicked.connect(self.play_song)
        self.DJ_next_button = self.music_player.make_button('player_icons\\next-song-icon.svg', 35, 35, color = None)
        self.DJ_next_button.clicked.connect(self.play_next)
        self.DJ_volium_slide = self.music_player.make_volume_bar()
        self.DJ_volium_slide.valueChanged.connect(self.handle_changed_value)
        self.DJ_volium_icon = self.music_player.make_volume_icon()

        ### Timer ###
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(lambda: self.music_player.updateProgressBar(self.DJ_progress_bar))
        


        ### Button Section ###
        self.DJ_add_song_container, self.DJ_add_song_box = self.make_container('Add Song', 'player_icons\plus-icon.svg', self.add_song_func)
        self.DJ_playlist_container, self.DJ_playlist_box = self.make_container('Playlist', 'player_icons\playlist-icon.svg', self.playlist_func)
        self.DJ_end_party_container, self.DJ_end_party_box = self.make_container('Close Party', 'player_icons\mute-icon.svg', self.end_party_func)
        self.DJ_add_local_song_container, self.DJ_add_local_song_box = self.make_container('Add Local Song', 'player_icons\search-icon.svg', self.add_local_song_func)
        

        ##### Left Part #####
        self.DJ_users_title = self.make_users_label()
        self.make_DJ_users_list()

    def DJ_room_layouts(self):
        self.DJ_main_layout = QHBoxLayout()
        self.DJ_main_layout_box = QGroupBox()
        self.DJ_main_layout_box.setLayout(self.DJ_main_layout)

        self.DJ_main_left_layout = QVBoxLayout()
        self.DJ_main_right_layout = QVBoxLayout()

        self.DJ_top_section = QVBoxLayout()
        self.DJ_top_section.addWidget(self.DJ_chat_button)

        self.DJ_song_section = QVBoxLayout()
        self.DJ_song_section.addWidget(self.DJ_song_name)
        self.DJ_song_section.addWidget(self.DJ_progress_bar)

        self.DJ_ctrl_section = QHBoxLayout()
        self.DJ_ctrl_section_box = QGroupBox()
        self.DJ_ctrl_section_box.setStyleSheet(style.DJ_ctrl_section())
        self.DJ_ctrl_section_box.setLayout(self.DJ_ctrl_section)
        self.DJ_ctrl_section.addWidget(self.DJ_like_button)
        self.DJ_ctrl_section.addWidget(self.DJ_previous_button)
        self.DJ_ctrl_section.addWidget(self.DJ_play_button)
        self.DJ_ctrl_section.addWidget(self.DJ_next_button)
        self.DJ_ctrl_section.addWidget(self.DJ_volium_slide)
        self.DJ_ctrl_section.addWidget(self.DJ_volium_icon)


        self.DJ_button_section = QHBoxLayout()
        self.DJ_button_section.addWidget(self.DJ_add_song_box)
        self.DJ_button_section.addWidget(self.DJ_playlist_box)
        self.DJ_button_section.addWidget(self.DJ_end_party_box)
        self.DJ_button_section.addWidget(self.DJ_add_local_song_box)


        self.DJ_main_layout.addLayout(self.DJ_main_left_layout)
        self.DJ_main_layout.addLayout(self.DJ_main_right_layout)

        self.DJ_main_left_layout.addLayout(self.DJ_top_section)
        self.DJ_main_left_layout.addLayout(self.DJ_song_section)
        self.DJ_main_left_layout.addWidget(self.DJ_ctrl_section_box)
        self.DJ_main_left_layout.addLayout(self.DJ_button_section)
        
        self.DJ_main_right_layout.addWidget(self.DJ_users_title)
        self.DJ_main_right_layout.addLayout(self.DJ_users_list)


    ######################### DJ Room UI ################################


# almog = DJ('almog999')