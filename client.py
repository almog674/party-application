import socket
import threading
import pickle
from chat import Chat_Data
from room import Room


class Client:
    def __init__(self):
        self.IP = socket.gethostbyname(socket.gethostname())
        self.PORT = 8888
        self.client = self.connect_client(self.IP, self.PORT)
        self.counter = 0
        self.latest_data = []
        self.new_messages = []

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

    def receive(self):
        while True:
            message = self.client.recv(1024).decode()
            print(message)
            self.counter += 1
            if len(self.latest_data) > 50:
                raise Exception('The data bucket is too big...')
            if '[OBJECT]' in message:
                message = self.client.recv(1024)
                message_clear = pickle.loads(message)
                if isinstance(message_clear, Chat_Data):
                    self.new_messages.append(message_clear)
                else:
                    self.latest_data.append(message_clear)

    def send_data(self, data):
        data_send_thread = threading.Thread(
            target=self.client.send, args=(str(data).encode(), ))
        data_send_thread.start()

    def connect_client(self, ip, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        return client
