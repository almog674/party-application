# from music_player import Music_Player
from labrary_base import *

class songs_fields_window(QWidget):
    def __init__(self, parent, username, mode):
        super().__init__()
        self.mode = mode
        self.setFixedSize(400, 300)
        self.setWindowTitle(self.mode)
        self.username = username
        self.parent = parent

        self.audio = None
        self.file_format = None

        self.UI()
        self.show()

    def addSongFile(self):
        self.file_dialog = QFileDialog.getOpenFileName(self, 'Add Sound', '', 'Sound Files (*.mp3 *.ogg *.wav)')
        # try:
        short_path = os.path.basename(self.file_dialog[0])
        filename = os.path.abspath(self.file_dialog[0])
        file_format_split = short_path.split('.')
        self.file_format = '.' + file_format_split[len(file_format_split) - 1]
        audio_code = open(filename , 'rb')
        data_array = []
        for line in audio_code:
            data_array.append(line)
        self.audio = data_array
        # except:
        #     pass

    def submit(self):
        song_name = self.song_name_field.text()
        artist_name = self.artist_name_field.text()
        if len(artist_name) == 0:
            artist_name = None
        if self.mode == 'Add Song':
            song_audio = self.audio
            file_format = self.file_format
            self.parent.add_song(song_name, artist_name, song_audio, file_format)
        data = self.parent.search_song(song_name, artist_name)
        

    def UI(self):
        self.main_layout = QVBoxLayout()

        self.title = QLabel(self.mode)
        self.song_name_field = QLineEdit()
        self.song_name_field.setPlaceholderText('Song name (required)')
        self.artist_name_field = QLineEdit()
        self.artist_name_field.setPlaceholderText('Artist name')
        self.add_song_button = QPushButton()
        self.add_song_button.clicked.connect(self.addSongFile)
        self.submit_button = QPushButton('Submit')

        self.submit_button.clicked.connect(self.submit)

        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.song_name_field)
        self.main_layout.addWidget(self.artist_name_field)
        if self.mode == 'Add Song':
            self.main_layout.addWidget(self.add_song_button)
        self.main_layout.addWidget(self.submit_button)

        self.setLayout(self.main_layout)