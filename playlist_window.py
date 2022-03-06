from labrary_base import *
from gui_helper import Gui_Helper
from reusible_widgets.playlist_button import Playlist_Button
# from music_player import Music_Player


class playlist_window(QWidget):
    def __init__(self, parent, username, database, admin = True):
        super().__init__()
        self.username = username
        self.admin = admin
        self.database = database
        self.setFixedSize(400, 400)
        self.setWindowTitle('Your Playlist')
        self.parent = parent
        self.favorits = False

        self.UI()
        self.show()

    def make_top_section(self):
        self.playlist_top_section, self.playlist_top_section_box = Gui_Helper.make_layout_full(self = self, style_function = style.empty, height = 80 , directon = 1)
        self.playlist_top_title = QLabel('All Playlist')
        self.playlist_top_title.setStyleSheet(style.playlist_title())
        self.playlist_top_button = Playlist_Button('player_icons\heart-icon.svg', self.show_only_favorits_toggle)

        self.playlist_top_section.addStretch(1)
        self.playlist_top_section.addWidget(self.playlist_top_title)
        self.playlist_top_section.addStretch(3)
        self.playlist_top_section.addWidget(self.playlist_top_button)
        self.playlist_top_section.addStretch(1)

    def UI(self):
        self.main_page = QVBoxLayout()
        self.main_page.setContentsMargins(QMargins(0,0,0,0))

        self.background, self.background_box = Gui_Helper.make_layout_full(self = self, style_function = style.playlist_backgound)

        self.make_top_section()

        self.playlist_main_layout, self.playlist_main_layout_box = Gui_Helper.make_layout_full(self = self, style_function = style.playlist_backgound, directon = 2)
        self.playlist_main_layout_box = Gui_Helper.make_layout_scrollable(self = self, layout = self.playlist_main_layout_box, vertical = True, height = False)
        self.playlist_main_layout_box.verticalScrollBar().hide()
        

        self.update_playlist()

        self.main_page.addWidget(self.background_box)
        self.background.addWidget(self.playlist_top_section_box)
        self.background.addWidget(self.playlist_main_layout_box)
        self.setLayout(self.main_page)

    def show_only_favorits_toggle(self, e):
        self.favorits = not self.favorits
        self.update_playlist()
        self.update_title()
        self.playlist_top_button.update_heart_icon(full = self.favorits)

    def update_title(self):
        if self.favorits:
            self.playlist_top_title.setText('Favorits')
        else:
            self.playlist_top_title.setText('All Playlist')

    def show_song_info(self, e):
        print('song info')

    def clear_playlist(self):
        for row in range(self.playlist_main_layout.rowCount()):
            if row:
                self.playlist_main_layout.removeRow(row)

    def update_playlist(self):
        favorits = self.database.get_liked_song(self.username)
        self.clear_playlist()
        for song in self.parent.play_list_now:
            if ((self.favorits == False) or (song['song_name'] in favorits)):
                if self.admin == True:
                    song_container, song_container_box, song_id, song_title, info_button, trash_button = self.build_song_container(song['id'], song['song_name'])
                else:
                    song_container, song_container_box, song_id, song_title, info_button = self.build_song_container(song['id'], song['song_name'])
                self.playlist_main_layout.addRow(song_container_box)


    def build_song_container(self, song_id, song_name):
        song_container, song_container_box = Gui_Helper.make_layout_full(self = self, style_function = style.playlist_container, height = 45 , directon = 1)

        song_id_label = QLabel(f'{song_id}')
        song_id_label.setStyleSheet(style.playlist_id())
        song_id_label.setFixedSize(30, 30)
        song_id_label.setAlignment(Qt.AlignHCenter)

        song_title = QLabel(song_name)
        song_title.setStyleSheet(style.playlist_window_label())
        info_button = Playlist_Button('player_icons\search-icon.svg', self.show_song_info, size = 30)

        if self.admin == True:
            trash_button = Playlist_Button('player_icons\\trash-icon.svg', lambda : self.parent.delete_song("2", song_id), size = 30)
            # trash_button.mouseReleaseEvent = lambda song_id, info_button: self.parent.delete_song(self = "2",event =  "#", index = song_id)

        song_container.addStretch(1)
        song_container.addWidget(song_id_label)
        song_container.addStretch(3)
        song_container.addWidget(song_title)
        song_container.addStretch(3)
        song_container.addWidget(info_button)
        song_container.addStretch(1)
        if self.admin == True:
            song_container.addWidget(trash_button)
            song_container.addStretch(1)
            return (song_container, song_container_box, song_id_label, song_title, info_button, trash_button)
        else:
            return (song_container, song_container_box, song_id_label, song_title, info_button)
