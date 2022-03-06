from Database import database
from client import Client
from threading import Thread
from main_two import Main
from labrary_base import *
from music_player import Music_Player


class Person:
    def __init__(self, name):
        self.name = name
        self.kicked = False
        self.socket_client = Client()
        self.database_tool = database()
        self.music_player = Music_Player(name)
        self.room = None
        self.counter = 0

    def get_current_time(self):
        time_now = time.strftime('%H:%M', time.gmtime())
        return time_now

    def build_message(self, name, code, text, receiver=None):
        date = self.get_current_time()
        message = {'name': name,  'code': code,
                   'text': text, 'date': date, 'receiver': receiver}
        return message

    def make_message_box(self, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.setFixedSize(100, 100)
        msg.exec()

    def make_special_message_box(self, text):
        box_thread = Thread(target=self.make_message_box, args=(text, ))
        box_thread.start()

    def send_message_to_server(self, name, code, text, receiver=None):
        message = self.build_message(name, code, text, receiver)
        self.socket_client.send_data(message)
