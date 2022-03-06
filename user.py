from main_two import Main
from labrary_base import *
from Database import database
from Person import Person
from room import Room
from time import sleep
import threading
from chat import Chat_Data, Chat_UI
from gui_threads import Gui_Thread_User

class User(QWidget, Person):
    def __init__(self, name):
        QWidget.__init__(self, name = name)
        self.playlist = []
        self.cursor = 0

        self.chat = None
        self.chat_data_thread = threading.Thread(target = self.check_chat_data)
        self.check_latest_data_thread = threading.Thread(target = self.check_latest_data)

    def UI(self):
        self.main_page = QHBoxLayout()
        self.setGeometry(150, 100, 950, 675)
        self.setWindowTitle("User Party")

        self.gui_thread = Gui_Thread_User()

        self.page_system = QStackedWidget()

        self.auth_room()
        self.waiting_room()
        self.make_user_party()

        self.page_system.addWidget(self.auth_main_layout_box)
        self.page_system.addWidget(self.waiting_main_layout_box)
        self.page_system.addWidget(self.user_main_layout_box)

        self.gui_thread.room_value.connect(self.go_to_page)
        self.gui_thread.start()
        self.gui_thread.go_to_page_0()

        self.main_page.addWidget(self.page_system)
        self.setLayout(self.main_page)
        self.check_latest_data_thread.start()
        self.show()


    def update_waiting_page(self):
        self.waiting_title.setText(self.room.name)
        if threading.main_thread() == threading.current_thread():
            self.build_waiting_users_grid()
        else:
            self.gui_thread.update_waiting_page.connect(self.update_waiting_page)
            self.gui_thread.update_waiting_page_func()
        self.waiting_code.setText(self.room.code)


    def build_waiting_users_grid(self):
        counter = 0
        self.gui_thread.delete_waiting_user_grid.connect(self.clear_waiting_users_grid)
        self.gui_thread.delete_waiting_grid()
        for user in self.room.users:
            container = self.build_waiting_users_single(user, counter)
            counter += 1
            self.waiting_users_grid.addLayout(container, counter, math.floor(counter / 5))

    def clear_waiting_users_grid(self):
        for i in reversed(range(self.waiting_users_grid.count())):
            self.delete_single_user_grid(self.waiting_users_grid.itemAt(i))

    def delete_single_user_grid(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.delete_single_user_grid(item.layout())

    def build_waiting_users_single(self, user, counter):
        container = QHBoxLayout()
        title = QLabel(user)

        container.addWidget(title)
        return container

    #################### Dealing With Multiple Pages #####################

    def go_to_page(self, value):
        page_number, page_geometry, page_title = value
        first, second, third, fourth = page_geometry
        self.page_system.setCurrentIndex(page_number)
        self.setGeometry(first, second, third, fourth)
        self.setWindowTitle(page_title)

    def go_to_waiting_page(self):
        self.gui_thread.go_to_page_1()
        self.gui_thread.room_value.connect(self.go_to_page)

    def go_to_auth_page(self):
        self.gui_thread.go_to_page_0()
        self.gui_thread.room_value.connect(self.go_to_page)

    def go_to_party_page(self):
        self.gui_thread.go_to_page_2()
        self.gui_thread.room_value.connect(self.go_to_page)

    #################### Dealing With Multiple Pages #####################

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
            if self.page_system.currentIndex() == 0:
                if self.room.is_active == False:
                    self.go_to_waiting_page()
                    self.update_waiting_page()
                else:
                    self.go_to_party_page()
            if self.page_system.currentIndex() == 1:
                self.update_waiting_page()
        elif isinstance(latest_data, dict):
            if latest_data['message_type']:
                if latest_data['message_type'] == '[KICK]':
                    message_text = latest_data["message_name"] + ' kicked you out at ' + latest_data["message_date"]
                    #################################### Need To Make A message Window For That!!! #########################
                    # print(message_text)
                    # self.make_message_box(message_text)
                    # sleep(3)
                    self.kicked = True
                    self.destroy_window()
                elif latest_data['message_type'] == 'popup':
                    self.make_popup(message_text)
                elif latest_data['message_type'] == '[ASK]':
                    self.gui_thread.make_message_box.connect(lambda: self.make_special_message_box('The DJ asks for your opinion'))
                    self.gui_thread.make_message_box_func()
                elif latest_data['message_type'] == '[PLAY]':
                    self.play_song(latest_data)
                elif latest_data['message_type'] == '[PLAYLIST]':
                    self.update_playlist(latest_data)
                elif latest_data['message_type'] == '[ACTIVATE]':
                    self.go_to_party_page()
                elif latest_data['message_type'] == '[FINISH]':
                    message_text = 'The party end:('
                    #################################### Need To Make A message Window For That!!! #########################
                    # print(message_text)
                    # self.make_message_box(message_text)
                    # sleep(3)
                    self.kicked = True
                    self.destroy_window()
        else:   
            print(f'latest data: {latest_data}')

    def update_playlist(self, playlist):
        self.playlist = eval(playlist['message'])
        self.song_builder = threading.Thread(target = self.build_songs)
        self.song_builder.start()

    def build_songs(self):
        new_playlist = []
        for index, song in enumerate(self.playlist):
            song_data = self.database_tool.search_song(song, None)
            song_data['id'] = index
            new_playlist.append(song_data)
        self.playlist = new_playlist
            
    def play_song(self, data):
        print(data['message'])

    def make_popup(self, text):
        popup = QHBoxLayout(self)
        popup.SetFixedSize(100, 100)

        popup_text = QLabel(text)
        popup_text.setStyleSheet(style.container_label())

        popup.addWidget(popup_text)
        popup.move(100,100)

    def like_song(self, event):
        self.send_message_to_server(self.name, 24, None)

    def dislike_song(self, event):
        self.send_message_to_server(self.name, 25, None)

    def playlist_func(self, event):
        self.music_player.open_playlist_window(None, False)
    
    def destroy_window(self, event = None):
        self.close()

    def closeEvent(self, event):
        if self.kicked == False:
            self.send_message_to_server(self.name, 4, None)
        self.kicked = True
        self.destroy_window()


    ################# Auth Room ################

    def auth_room(self):
        self.auth_room_widgets()
        self.auth_room_layouts()

    def auth_room_widgets(self):
        self.auth_room_title = QLabel('Join Party!')
        self.auth_username_container, self.auth_username_title, self.auth_username_edit = self.make_input_container('Room Name: ')
        self.auth_code_container, self.auth_code_title, self.auth_code_edit = self.make_input_container('Room Code: ')
        self.auth_submit_button = QPushButton('Submit')
        self.auth_submit_button.clicked.connect(self.auth_join_party)

    def auth_room_layouts(self):
        self.auth_main_layout = QVBoxLayout()
        self.auth_main_layout_box = QGroupBox()
        # self.auth_main_layout_box.setStyleSheet(style.auth_main_layout_box())
        self.auth_main_layout_box.setLayout(self.auth_main_layout)

        self.auth_main_layout.addWidget(self.auth_room_title)
        self.auth_main_layout.addLayout(self.auth_username_container)
        self.auth_main_layout.addLayout(self.auth_code_container)
        self.auth_main_layout.addWidget(self.auth_submit_button)


    def make_input_container(self, text):
        container = QHBoxLayout()
        title = QLabel(text)
        edit = QLineEdit()

        container.addWidget(title)
        container.addWidget(edit)
        return container, title, edit

    def auth_join_party(self):
        room_name = self.auth_username_edit.text()
        room_code = self.auth_code_edit.text()
        if len(room_name) == 0:
            self.make_message_box('You need the specify a name...')
            return
        if len(room_code) != 8:
            self.make_message_box('The code needs to be 8 letters long...')
            return
        data_to_send = f'{room_name}/{room_code}'
        self.send_message_to_server(self.name, 14, data_to_send)
        # sleep(1)
        # response = self.socket_client.latest_data
        # if not isinstance(response, Room):
        #     self.make_message_box(f'the actual response is {response}')
        # else:
        #     self.room = response
        #     print(self.room.users)

    ################# Auth Room ################

    ################# Waiting Room ################
    def waiting_room(self):
        self.waiting_room_widgets()
        self.waiting_room_layouts()

    def waiting_room_widgets(self):
        self.waiting_exit_button = QPushButton('EXIT')
        self.waiting_exit_button.clicked.connect(self.closeEvent)
        
        self.waiting_title = QLabel('Title')
        self.waiting_code = QLabel('Code')

    def waiting_room_layouts(self):
        self.waiting_main_layout = QVBoxLayout()
        self.waiting_main_layout_box = QGroupBox()
        self.waiting_main_layout_box.setLayout(self.waiting_main_layout)

        self.waiting_top_layout = QHBoxLayout()

        self.waiting_top_right_layout = QVBoxLayout()

        self.waiting_users_grid = QGridLayout()
        self.waiting_users_grid_box = QGroupBox()
        self.waiting_users_grid_box.setStyleSheet(style.waiting_users_grid_box())
        self.waiting_users_grid_box.setLayout(self.waiting_users_grid)

        ##### Adding the nested layouts #####
        self.waiting_main_layout.addLayout(self.waiting_top_layout, 30)
        self.waiting_main_layout.addWidget(self.waiting_users_grid_box, 70)

        self.waiting_top_layout.addWidget(self.waiting_exit_button)
        self.waiting_top_layout.addLayout(self.waiting_top_right_layout)

        self.waiting_top_right_layout.addWidget(self.waiting_title)
        self.waiting_top_right_layout.addWidget(self.waiting_code)
        ################# Waiting Room ################

    ######################### Party Room Special Widgets ################################
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
        container_icon.setPixmap(QPixmap('user-solid.svg'))
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

    def make_user_users_list(self):
        like = False
        hate = False
        self.user_users_list = QVBoxLayout()
        if self.room:
            # self.gui_thread.delete_user_users_list.connect(lambda: self.clear_layout(self.user_main_right_layout))
            # self.gui_thread.delete_user_users_list_func()
            for user in self.room.users:
                print(user)
                if user in self.room.like_users:
                    like = True
                if user in self.room.hate_users:
                    hate = True
                user_container = self.make_user_single(user, like = like, hate = hate)
                self.user_users_list.addLayout(user_container)
            self.user_main_right_layout.addWidget(self.user_users_title)
            self.user_main_right_layout.addLayout(self.user_users_list)
        

    ######################### Party Room Special Widgets ################################



    ################# User Party ################
    def make_user_party(self):
        self.make_user_party_widgets()
        self.make_user_party_layouts()

    def make_user_party_widgets(self):
        ###### Right Part #####
        ### Top Section ###
        self.user_chat_button = QPushButton('Open Chat')
        self.user_chat_button.clicked.connect(self.open_chat)

        ### Song Section ###
        self.user_song_name = QLabel('Nothing yet...')
        self.user_progress_bar = self.music_player.make_progress_bar()
        self.user_volium_slide = self.music_player.make_volume_bar()
        self.user_volium_icon = self.music_player.make_volume_icon()
        


        ### Button Section ###
        self.user_like_song_container, self.user_like_song_box = self.make_container('Like Song', 'player_icons\heart-full-icon.svg', self.like_song)
        self.user_dislike_container, self.user_dislike_box = self.make_container('Dislike', 'player_icons\\trash-icon-icon.svg', self.dislike_song)
        self.user_playlist_container, self.user_playlist_party_box = self.make_container('Playlist', 'player_icons\playlist-icon.svg', self.playlist_func)
        self.user_quit_container, self.user_quit_party_box = self.make_container('Quit Party', 'player_icons\mute-icon.svg', self.destroy_window)
       
        

        ##### Left Part #####
        self.user_users_title = self.make_users_label()
        self.make_user_users_list()

    def make_user_party_layouts(self):
        self.user_main_layout = QHBoxLayout()
        self.user_main_layout_box = QGroupBox()
        self.user_main_layout_box.setLayout(self.user_main_layout)

        self.user_main_left_layout = QVBoxLayout()
        self.user_main_right_layout = QVBoxLayout()

        self.user_top_section = QVBoxLayout()
        self.user_top_section.addWidget(self.user_chat_button)

        self.user_song_section = QVBoxLayout()
        self.user_song_section.addWidget(self.user_song_name)
        self.user_song_section.addWidget(self.user_progress_bar)
        self.volium_layout = QHBoxLayout()
        self.volium_layout.addWidget(self.user_volium_slide)
        self.volium_layout.addWidget(self.user_volium_icon)
        self.user_song_section.addLayout(self.volium_layout)


        self.user_button_section = QHBoxLayout()
        self.user_button_section.addWidget(self.user_like_song_box)
        self.user_button_section.addWidget(self.user_dislike_box)
        self.user_button_section.addWidget(self.user_playlist_party_box)
        self.user_button_section.addWidget(self.user_quit_party_box)


        ### Adding the nested layouts ###
        self.user_main_layout.addLayout(self.user_main_left_layout)
        self.user_main_layout.addLayout(self.user_main_right_layout)

        self.user_main_left_layout.addLayout(self.user_top_section)
        self.user_main_left_layout.addLayout(self.user_song_section)
        self.user_main_left_layout.addLayout(self.user_button_section)

        self.user_main_right_layout.addWidget(self.user_users_title)
        self.user_main_right_layout.addLayout(self.user_users_list)

    ################# User Party ################