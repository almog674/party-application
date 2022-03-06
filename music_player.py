from main_two import Main
from labrary_base import *
from pygame import mixer
from songs_fields_window import songs_fields_window
from playlist_window import playlist_window
from gui_helper import Gui_Helper

class Music_Player(Main):
    play_list_now = []
    song_index = 0
    need_audio = True

    def __init__(self, username, parent = None):
        QWidget.__init__(self)
        self.username = username
        self.parent = parent
        self.database = database()
        self.get_initial_values_db()
        self.spotiy_client = spotifyAPI(client_id = '9c8a8a4cfe9c492a86eced46e6ac829b', client_secret = '6d71b04b746c4ca6bb548f79a13bfb26')
        self.url_conventer = url_to_image()

        self.music_player = mixer
        self.music_player.init()
        self.music_player.music.set_volume(0.7)
        self.print_play_list_now()
        
        self.current_song = None
        self.prograss_bar_count = 0


        self.file_index = 0
        self.current_file = None
        self.prev_file = None
        self.song_duration = None
        
        self.volume = 70
        self.playing = False




    def UI(self):
        self.make_widgets()
        self.make_layouts()
        self.setLayout(self.main_page)
        self.show()

    #################### Database Stuff #####################
    def get_initial_values_db(self):
        self.password, self.email, self.playlist = self.database.get_user_values(self.username)

    def check_if_song_liked(self):
        pass

    def search_song(self, song_name, song_artist):
        full_data = self.database.search_song(song_name, song_artist)
        if full_data == None:
            self.make_message_box(f'There is no song called {song_name}')
            return
        for song in self.play_list_now:
            if full_data['song_name'] == song['song_name']:
                self.make_message_box(f'This Song is already added to the playlist')
                return
        if len(self.play_list_now) == 10:
            self.make_message_box(f'The playlist is full, if you want to add new song please delete one')
            return
        self.play_list_now.append(full_data)
        full_data['id'] = self.play_list_now.index(full_data)
        self.print_play_list_now()
        return full_data

    def add_song(self, song_name, song_artist, song_audio, file_format):
        song_name, artist_name, song_duration, background_url = self.collect_song_spotify_data(song_name, song_artist)
        username = self.username
        self.database.add_song(song_name = song_name, audio = song_audio, duration = song_duration, background_url = background_url, user_name = username, file_format = file_format, artist = artist_name)

    #################### Database Stuff #####################






    #################### Logistic Functions #####################
    def make_message_box(self, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.setFixedSize(100,100)
        msg.exec_()
    
    def get_duration_format(self, duration):
        min, sec = divmod(duration, 60)
        if len(str(sec)) == 1:
            sec = '0' + str(sec)
        duration = f'{min}:{sec}'
        return duration

    def updateProgressBar(self, progress_bar):
        self.prograss_bar_count += 1
        progress_bar.setValue(self.prograss_bar_count)
        count_display = self.get_duration_format(self.prograss_bar_count)
        song_duration_display = self.get_duration_format(self.song_duration)
        progress_bar.setFormat(f'{count_display} / {song_duration_display}')
        if self.prograss_bar_count == self.song_duration:
            self.timer.stop()

    def print_play_list_now(self):
        if len(self.play_list_now) == 0:
            print('The playlist is empty')
            return
        for song in self.play_list_now:
            print('Song number: ' +  str(song['id']) + " " + song['song_name'])

    def update_play_button(self, button):
        icon = QPixmap('player_icons\play-icon.svg')
        if self.playing == True:
                icon = QPixmap('player_icons\pause-icon.svg')
        mask = icon.createMaskFromColor(QColor('black'), Qt.MaskOutColor)
        icon.fill(QColor('red'))
        icon.setMask(mask)
        button.setIcon(QIcon(icon))
        

    def update_song_label(self, song_name, artist, label):
        label.setText(f'{song_name} - {artist}')

    def update_song_indexes(self):
        for song in self.play_list_now:
            song['id'] = self.play_list_now.index(song)


    def collect_song_spotify_data(self, song_name, song_artist):
        song_data = self.spotiy_client.search(query = song_name, search_type = 'track', option_number = 0 , expected_artist = song_artist)
        song_name = song_data['song_name']
        artist_name = song_data['artist_name']
        song_duration = song_data['song_duration']
        background_url = song_data['background_url']
        return song_name, artist_name, song_duration, background_url

    def change_song_background(self, song_url):
        song_url = self.current_song['background_url']
        image = self.url_conventer.convert_url(song_url)
        name = 'background_image.jpg'
        background_picture = open(name, 'wb')
        background_picture.write(image.read())

        backgorund = QPixmap(name)
        backgorund.scaled(350,200, Qt.KeepAspectRatio)
        self.song_backgorund.setPixmap(backgorund)
        self.main_top_layout_box.setStyleSheet('QGroupBox {border-image: url("' + name + '") 0 0 0 0 stretch stretch; background-repeat: no-repeat;}')

    def change_song(self, mode, function):
        if mode == -1:
            if Music_Player.song_index == 0:
                self.make_message_box("You can't go to the song at number -1")
            else:
                Music_Player.song_index -= 1
                Music_Player.need_audio = True
                function()
        else:
            if Music_Player.song_index >= (len(self.play_list_now) - 1):
               self.make_message_box("There is no song at this point")
            else: 
                Music_Player.song_index += 1
                Music_Player.need_audio = True
                function()

    def delete_song(self, event, index):
        # print(self)
        # print(event)
        # print(f'index {index}')
        ### Delete a song from the play list ###
        if (index == Music_Player.song_index) and (index != 0):
            self.make_message_box("You Can't Delete The song you hearing right now")
            return

        Music_Player.song_index = 0
        Music_Player.need_audio = True
        # print(f'Set the current song index of {self} to {Music_Player.song_index}')
        self.play_list_now.remove(self.play_list_now[index])
        self.update_song_indexes()
        # print(f'Set the current song index to {Music_Player.song_index}')
        


    def like_song(self):
        if self.current_song == None:
            return
        self.database.like_song(self.current_song['song_name'], self.username)
        self.get_initial_values_db()
        self.update_like_button()

    def handle_changed_value(self):
        self.update_volume_icon(self.volume_slider, self.volume_icon)
        self.music_player.music.set_volume(self.volume_slider.value() / 100)
    

    def get_song_duration_progbar(self, song):
        duration = song['duration']
        minute, seconds = duration.split(':')
        minute = int(minute) * 60
        seconds = int(seconds)
        duration = minute + seconds
        return duration

    def play_song(self):
        if self.playing == True:
            self.music_player.music.pause()
            self.playing = False
            self.update_play_button(self.play_button)
            self.timer.stop()
        else:
            if len(self.play_list_now) == 0:
                self.make_message_box('Please insert songs before playing')
                return
            song_data = self.play_list_now[Music_Player.song_index]
            self.current_song = self.play_list_now[Music_Player.song_index]
            if Music_Player.need_audio == True:
                audio = self.extract_audio_data(song_data)
                self.music_player.music.load(audio)
                Music_Player.need_audio = False
                self.music_player.music.play()
                self.play_song_update_ui(song_data, True)
            else:
                self.play_song_update_ui(song_data, False)
                self.music_player.music.unpause()
            self.playing = True
            self.update_play_button(self.play_button)

    def play_song_not_locally(self, play_button, progress_bar, timer, title):
        if self.playing == True:
            self.music_player.music.pause()
            self.playing = False
            self.update_play_button(play_button)
            timer.stop()
        else:
            if len(self.play_list_now) == 0:
                self.make_message_box('Please insert songs before playing')
                return
            # print(f'song_index of {self}: {Music_Player.song_index}')
            song_data = self.play_list_now[Music_Player.song_index]
            self.current_song = self.play_list_now[Music_Player.song_index]
            if Music_Player.need_audio == True:
                self.update_song_label(song_data['song_name'], song_data['artist'], title)
                audio = self.extract_audio_data(song_data)
                self.music_player.music.load(audio)
                Music_Player.need_audio = False
                self.music_player.music.play()
                progress_bar.setValue(0)
                self.song_duration = self.get_song_duration_progbar(song_data)
                progress_bar.setMaximum(self.song_duration)
                self.prograss_bar_count = 0
            else:
                self.music_player.music.unpause()
            timer.start()
            self.playing = True


    def play_song_update_ui(self, song_data, need_audio):
        if need_audio == True:
            self.update_song_label(song_data['song_name'], song_data['artist'], self.song_title)
            self.song_progress_bar.setValue(0)
            self.song_duration = self.get_song_duration_progbar(song_data)
            self.song_progress_bar.setMaximum(self.song_duration)
            self.prograss_bar_count = 0
        self.timer.start()
        self.update_like_button()
        self.change_song_background(song_data['background_url'])
            

    def extract_audio_data(self, song_data):
        file_name = 'audio_file' + song_data['file_format']
        file_audio = song_data['audio']
        if self.current_file:
            self.music_player.music.unload()
        with open(file_name, 'wb') as self.current_file:
            for line in file_audio:
                self.current_file.write(line)
        return file_name

    def go_to_homepage(self, a):
        self.parent.go_to_page(0)

    def open_search_song_window(self, a):
        self.search_window = songs_fields_window(self, self.username, 'Search Song')

    def open_add_song_window(self, a):
        self.search_window = songs_fields_window(self, self.username, 'Add Song')
    
    def open_playlist_window(self, a, admin = True):
        self.playlist_window = playlist_window(self, self.username, self.database, admin)


    def update_volume_icon(self, slider, icon):
        if slider.value() == 0:
            icon.setIcon(QIcon('player_icons\mute-icon.svg'))
        elif slider.value() < 50:
            icon.setIcon(QIcon('player_icons\\volume-low-icon.svg'))
        else:
            icon.setIcon(QIcon('player_icons\\volume-high-icon.svg'))

    #################### Logistic Functions #####################








    #################### Special Widgets #####################
    def get_background_image(self):
        number = random.randint(1, 6)
        song_background = QPixmap('background-' + str(number) + '.jpg')
        song_background.scaled(425,250, Qt.KeepAspectRatio)
        self.song_backgorund.setPixmap(song_background)
        self.main_top_layout_box.setStyleSheet('QGroupBox {border-image: url("background-' + str(number) + '.jpg") 0 0 0 0 stretch stretch; background-repeat: no-repeat;}')

    def make_container(self, text, path, function):
        container = QHBoxLayout()
        container_box = QGroupBox()
        container_box.setFixedSize(200,75)
        container_box.setCursor(Qt.PointingHandCursor)
        container_box.setLayout(container)
        container_box.setStyleSheet(style.continer())

        label = QLabel(text)
        label.setStyleSheet(style.container_label())

        label_icon = QPushButton()
        label_icon.setIcon(QIcon(path))
        label_icon.setIconSize(QSize(30, 30))
        label_icon.setStyleSheet(style.like_button())

        container_box.mouseReleaseEvent = function
        label.mouseReleaseEvent = function
        label_icon.mouseReleaseEvent = function

        container.addWidget(label_icon)
        container.addWidget(label)
        return container, container_box, label, label_icon

    def make_button(self, path, width, height, color = None):
        button = QPushButton()
        icon = QPixmap(path)
        if color != None:
            mask = icon.createMaskFromColor(QColor('black'), Qt.MaskOutColor)
            icon.fill(QColor(color))
            icon.setMask(mask)
        button.setCursor(Qt.PointingHandCursor)
        button.setIcon(QIcon(icon))
        button.setFixedSize(width, height)
        button.setIconSize(QSize(width,height))
        return button

    def update_like_button(self):
        icon = QPixmap('player_icons\heart-icon.svg')
        if self.current_song != None:
            if self.current_song['song_name'] in self.playlist:
                icon = QPixmap('player_icons\heart-full-icon.svg')
        mask = icon.createMaskFromColor(QColor('black'), Qt.MaskOutColor)
        icon.fill(QColor('red'))
        icon.setMask(mask)
        self.like_button.setIcon(QIcon(icon))

    def make_like_button(self):
        button = self.make_button(path = 'player_icons\heart-icon.svg', width = 40, height = 40, color = 'red')
        button.setStyleSheet(style.like_button())
        button.clicked.connect(self.like_song)
        return button

    def make_play_button(self):
        button = self.make_button(path = 'player_icons\play-icon.svg', width = 40, height = 40, color = 'red')
        button.setFixedSize(60,60)
        button.setStyleSheet(style.play_song_button())
        button.clicked.connect(self.play_song)
        return button

    def make_next_button(self):
        button = self.make_button(path = 'player_icons\\next-song-icon.svg', width = 40, height = 40, color = 'red')
        button.setStyleSheet(style.like_button())
        button.clicked.connect(lambda: self.change_song(1, self.play_song))
        return button

    def make_previous_button(self):
        button = self.make_button(path = 'player_icons\previous-song-icon.svg', width = 40, height = 40, color = 'red')
        button.setStyleSheet(style.like_button())
        button.clicked.connect(lambda: self.change_song(-1, self.play_song))
        return button

    def make_volume_icon(self):
        button = self.make_button(path = 'player_icons\\volume-high-icon.svg', width = 40, height = 40, color = '#ddd')
        button.setStyleSheet(style.like_button())
        return button

    def make_volume_bar(self):
        slider = QSlider(Qt.Horizontal)
        slider.setToolTip('Volume')
        slider.setValue(70)
        slider.setMaximum(100)
        slider.setMinimum(0)
        slider.setFixedWidth(150)
        slider.setStyleSheet(style.volume_slider())
        return slider

    def make_progress_bar(self):
        progress_bar = QProgressBar()
        progress_bar.setStyleSheet(style.progress_bar())
        progress_bar.setFormat(f'0:00 / 0:00')
        progress_bar.setFixedWidth(425)
        progress_bar.setAlignment(Qt.AlignCenter)
        return progress_bar

    #################### Special Widgets #####################








    def make_widgets(self):
        ### Make The right top part ###
        self.homepage_container, self.homepage_container_box, self.homepage_container_label, self.homepage_container_icon = self.make_container('Home Page', 'player_icons\home-icon.svg', self.go_to_homepage)
        self.search_container, self.search_container_box, self.search_container_label, self.search_container_icon = self.make_container('Search Song', 'player_icons\search-icon.svg', self.open_search_song_window)
        self.add_container, self.add_container_box, self.add_container_label, self.add_container_icon = self.make_container('Add Song', 'player_icons\plus-icon.svg', self.open_add_song_window)
        self.playlist_container, self.playlist_container_box, self.playlist_container_label, self.playlist_container_icon = self.make_container('Playlist', 'player_icons\playlist-icon.svg', self.open_playlist_window)


        ### Make the card ###
        self.song_title = QLabel('Song Title - Song Artist')
        self.song_title.setStyleSheet(style.music_player_song_title())
        self.song_backgorund = QLabel()
        self.song_backgorund.setFixedSize(425,250)
        self.song_backgorund.setStyleSheet(style.song_background())
        self.song_progress_bar = self.make_progress_bar()
        
        

        ### Make The Bottom part ###
        self.like_button = self.make_like_button()
        self.previous_button = self.make_previous_button()
        self.play_button = self.make_play_button()
        self.next_button = self.make_next_button()
        self.volume_slider = self.make_volume_bar()
        self.volume_slider.valueChanged.connect(self.handle_changed_value)
        self.volume_icon = self.make_volume_icon()


        ### Timer ###
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(lambda: self.updateProgressBar(self.song_progress_bar))


    def make_layouts(self):
        self.main_page = QVBoxLayout()
        self.main_page.setContentsMargins(QMargins(0,0,0,0))

        self.main_layout, self.main_layout_box = Gui_Helper.make_layout_full(self = self, style_function = style.empty)

        self.main_top_layout, self.main_top_layout_box = Gui_Helper.make_layout_full(self = self, style_function = style.empty, directon = 1)
        self.get_background_image()

        self.main_bottom_layout, self.main_bottom_layout_box = Gui_Helper.make_layout_full(self = self, style_function = style.player_bottom_layout, directon = 1)
        self.top_left_layout = QHBoxLayout()
        self.top_right_layout, self.top_right_layout_box = Gui_Helper.make_layout_full(self = self, style_function = style.player_top_right)
        self.song_card_layout, self.song_card_layout_box = Gui_Helper.make_layout_full(self = self, style_function = style.player_song_card, width= 600, height= 400)


        self.main_page.addWidget(self.main_layout_box)
        self.main_layout.addWidget(self.main_top_layout_box, 85)
        self.main_layout.addWidget(self.main_bottom_layout_box, 15)

        self.main_top_layout.addLayout(self.top_left_layout, 70)
        self.main_top_layout.addWidget(self.top_right_layout_box, 30)


        ### Build the right top part ###
        self.top_right_layout.setAlignment(Qt.AlignRight)
        self.top_right_layout.addStretch(1)
        self.top_right_layout.addWidget(self.homepage_container_box)
        self.top_right_layout.addStretch(1)
        self.top_right_layout.addWidget(self.search_container_box)
        self.top_right_layout.addStretch(1)
        self.top_right_layout.addWidget(self.add_container_box)
        self.top_right_layout.addStretch(1)
        self.top_right_layout.addWidget(self.playlist_container_box)
        self.top_right_layout.addStretch(10)

        ### Build the card ###
        self.top_left_layout.addStretch()
        self.top_left_layout.addWidget(self.song_card_layout_box)
        # self.top_left_layout.addStretch()
        self.song_card_layout.addStretch(2)
        self.song_card_layout.addWidget(self.song_title, alignment = Qt.AlignHCenter)
        self.song_card_layout.addStretch(2)
        self.song_card_layout.addWidget(self.song_backgorund, alignment = Qt.AlignHCenter)
        self.song_card_layout.addStretch(2)
        self.song_card_layout.addWidget(self.song_progress_bar, alignment = Qt.AlignHCenter)
        self.song_card_layout.addStretch(2)


        ### Build the bottom part ###
        self.main_bottom_layout.addStretch(1)
        self.main_bottom_layout.addWidget(self.like_button)
        self.main_bottom_layout.addStretch(13)
        self.main_bottom_layout.addWidget(self.previous_button)
        self.main_bottom_layout.addStretch(4)
        self.main_bottom_layout.addWidget(self.play_button)
        self.main_bottom_layout.addStretch(4)
        self.main_bottom_layout.addWidget(self.next_button)
        self.main_bottom_layout.addStretch(4)
        self.main_bottom_layout.addWidget(self.volume_slider)
        self.main_bottom_layout.addStretch(1)
        self.main_bottom_layout.addWidget(self.volume_icon)
        self.main_bottom_layout.addStretch(1)