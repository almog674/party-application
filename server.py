import socket
import time
import threading
import pickle
from main_two import Main
from room import Room
from chat import Chat_Data


class Server():
    def __init__(self):
        self.IP = socket.gethostbyname(socket.gethostname())
        self.PORT = 8888
        self.server = self.connect_server()
        self.rooms = []
        self.clients = []

        while True:
            time.sleep(1)
            client = self.handle_connection(self.server)

    def connect_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', 8888))
        server.listen()
        print('Server is up and ready')
        return server

    def split_message(self, message):
        return message['name'], message['code'], message['text'], message['receiver'], message['date']

    def handle_connection(self, server):
        client, address = server.accept()
        print(f'Client connected at {address}')
        thread = threading.Thread(target=self.handle_client, args=(client, ))
        thread.start()
        # check_available_thread = threading.Thread(target = self.check_available_clients, args = (client, ))
        # check_available_thread.start()
        print(f'There are {threading.activeCount() - 1} active connections')
        return client

    def handle_client(self, client):
        while True:
            message = client.recv(1024).decode()
            message = eval(message)
            message_name, message_code, message_text, message_reciever, message_date = self.split_message(
                message)
            print(message_name, message_code, message_text,
                  message_reciever, message_date)
            if message_code == 4:
                self.user_exit(message_name, client, message_date)
            if message_code == 5:
                self.kick_user(message_name, client,
                               message_reciever, message_date)
            if message_code == 10:
                room = self.open_new_room(message_name, client)
                self.send_room(room, client)
            if message_code == 11:
                self.activate_room(message_name, client)
            if message_code == 12:
                self.change_room_code_server(message_name, client)
            if message_code == 13:
                self.change_room_name_server(
                    message_name, client, message_text)
            if message_code == 14:
                self.join_room_server(
                    message_name, client, message_text, message_date)
            if message_code == 15:
                self.close_room(message_name, client,
                                message_text, message_date)
            if message_code == 16:
                self.ask_for_opinion(message_name, client,
                                     message_text, message_date)
            if message_code == 20:
                self.update_playlist(message_name, client,
                                     message_text, message_date)
            if message_code == 21:
                self.play_song(message_name, client,
                               message_text, message_date)
            if message_code == 24:
                self.like_song(message_name, client, True)
            if message_code == 25:
                self.like_song(message_name, client, False)
            if message_code == 31:
                self.send_chat_message(
                    message_name, message_text, client, 'messages')

    def send_chat_message(self, message_name, message_text, client, channel):
        room = self.find_room_with_client(client)
        if channel == 'messages':
            room.chat.messages.append(message_text)
        else:
            room.chat.notefications.append(message_text)
        clients_to_send = self.find_clients_in_room(room)
        for client in clients_to_send:
            if isinstance(client, dict):
                client = client['client']
            client.send('[OBJECT]'.encode())
            time.sleep(0.05)
            chat = pickle.dumps(room.chat)
            client.send(chat)

    def like_song(self, message_name, client, like):
        room = self.find_room_with_client(client)
        if like == True:
            if message_name not in room.like_users:
                room.like_users.append(message_name)
            else:
                room.like_users.remove(message_name)
        else:
            if message_name not in room.hate_users:
                room.hate_users.append(message_name)
            else:
                room.hate_users.remove(message_name)
        self.send_room_broadcast(room)

    def ask_for_opinion(self, message_name, client, message_text, message_date):
        room = self.find_room_with_client(client)
        message_text = self.make_message_chat_server(
            f'{message_name} asks for your opinion', message_date)
        self.send_chat_message('[SERVER]', message_text,
                               client, 'notefications')

    def close_room(self, message_name, client, message_text, message_date):
        room = self.find_room_with_client(client)
        self.send_broadcast_message(
            room, client, message_text, message_name, '[FINISH]', message_date)
        self.rooms.remove(room)

    def play_song(self, message_name, client, message_text, message_date):
        # Get the room
        room = self.find_room_with_client(client)

        self.send_broadcast_message(
            room, client, message_text, message_name, '[PLAY]', message_date)

    def update_playlist(self, message_name, client, message_text, message_date):
        # Get ther room
        room = self.find_room_with_client(client)

        self.send_broadcast_message(
            room, client, message_text, message_name, '[PLAYLIST]', message_date)

    def activate_room(self, message_name, client):
        # Get the room
        room = self.find_room_with_client(client)

        # Check if the room is already active
        if room.is_active == True:
            return

        # Activate the room
        room.is_active = True

        # Build a clients list of the room
        clients_to_send = self.find_clients_in_room(room)

        # Send an activate message to all the clients
        for client in clients_to_send:
            self.send_privet_message(
                client['client'], None, '[ACTIVATE]', message_name, None)

        # Send the room in broadcast
        self.send_room_broadcast(room)

    def find_room_with_client(self, client):
        # Get the room
        room = None

        for one_client in self.clients:
            if one_client['client'] == client:
                room = one_client['room']
                return room

    def find_user_in_room(self, room, message_name):
        new_list = [x for x in self.clients if x['room'] == room]
        index = room.users.index(message_name)
        user = new_list[index]
        return user

    def kick_user(self, message_name, client, message_reciever, message_date):
        if message_name == message_reciever:
            self.send_privet_message(
                client, '[SERVER] you cannot kick yourself', 'error', message_name, message_date)
            return

        # Get the room
        room = self.find_room_with_client(client)

        # Get The user that we want to kick
        user_to_kick = self.find_user_in_room(room, message_reciever)

        # Send a message for all the other clients
        message = message_name + ' kicked ' + message_reciever
        message_text = self.make_message_chat_server(message, message_date)
        self.send_chat_message('[SERVER]', message_text,
                               client, 'notefications')

        # Send a message to the user
        self.send_privet_message(
            user_to_kick, None, '[KICK]', message_name, message_date)
        self.kick_user_from_room(
            room, user_to_kick, message, message_reciever, message_date)

        # Updating the rooms
        self.send_room_broadcast(room)

    def kick_user_from_room(self, room, client, message_text, message_name, message_date, kick=True):
        # Remove the user from all the lists
        # try:
        self.clients.remove(client)
        room.users.remove(message_name)
        # except Exception as error:
        #     print(error)

    def user_exit(self, message_name, client, message_date):
        # Get the room of the client
        room = self.find_room_with_client(client)

        # Check if it needed to remove from the lists
        if message_name not in room.users:
            print('succed')
            return

        # Get The user that we want to kick
        user_to_kick = self.find_user_in_room(room, message_name)

        # Send a message for all the other clients
        message = f'{message_name} has left the chat'
        message_text = self.make_message_chat_server(message, message_date)
        self.send_chat_message('[SERVER]', message_text,
                               client, 'notefications')

        # Delete the user from the lists
        message_text = message_name + ' quit out at ' + message_date
        self.kick_user_from_room(
            room, user_to_kick, message_text, message_name, message_date)

        # Updating the rooms
        self.send_room_broadcast(room)

    def send_privet_message(self, client, message, message_type, message_name, message_date):
        message = self.build_message_to_user(
            message, message_type, message_name, message_date)
        message = pickle.dumps(message)
        if not isinstance(client, socket.socket):
            client = client['client']
        client.send('[OBJECT]'.encode())
        time.sleep(0.05)
        client.send(message)

    def build_message_to_user(self, message, message_type, message_name, message_date):
        message = {'message': message, 'message_type': message_type,
                   'message_name': message_name, 'message_date': message_date}
        return message

    def make_message_chat_server(self, text, message_date):
        message = {
            'message_name': '[SERVER]',
            'message_text': text,
            'message_date': message_date
        }
        return message

    def join_room_server(self, message_name, client, message_text, message_date):
        room_name, room_code = message_text.split('/')
        error = None
        for room in self.rooms:
            if room.name == room_name:
                if room.code == room_code:
                    room.users.append(message_name)
                    client_dict = self.make_client_dict(client, room)
                    self.clients.append(client_dict)
                    message_text = self.make_message_chat_server(
                        f'{message_name} joined the chat', message_date)
                    self.send_chat_message(
                        '[SERVER]', message_text, client, 'notefications')
                    time.sleep(0.05)
                    self.send_room_broadcast(room)
                    return
                else:
                    error = '[ERROR] The room code is wrong...'
        if error == None:
            error = '[ERROR] There is no room with this name...'
        client.send(error.encode())

    def change_room_code_server(self, message_name, client):
        for room in self.rooms:
            if room.DJ == message_name:
                code = room.get_room_code()
                room.code = code
                self.send_room_broadcast(room)

    def change_room_name_server(self, message_name, client, text):
        for room in self.rooms:
            if room.DJ == message_name:
                room.name = text
                self.send_room_broadcast(room)

    def open_new_room(self, message_name, client):
        new_room = Room(message_name)
        new_room.users.append(message_name)
        client_dict = self.make_client_dict(client, new_room)
        self.clients.append(client_dict)
        self.rooms.append(new_room)
        return new_room

    def make_client_dict(self, client, room):
        return {'client': client, 'room': room}

    def send_room(self, room, client):
        if isinstance(client, dict):
            client = client['client']
        new_room_send = pickle.dumps(room)
        client.send('[OBJECT]'.encode())
        client.send(new_room_send)

    def send_room_broadcast(self, room):
        clients_to_send = self.find_clients_in_room(room)
        for client in clients_to_send:
            self.send_room(room, client)

    def find_clients_in_room(self, room):
        clients_to_send = []
        for client in self.clients:
            if client['room'] == room:
                clients_to_send.append(client)
        return clients_to_send

    def send_broadcast_message(self, room, client, message, message_name, message_type, message_date):
        # Make a list of all the relevent clients
        clients_to_send = self.find_clients_in_room(room)

        # Build the data that needed to send
        full_message = self.build_message_to_user(
            message, message_type, message_name, message_date)
        full_message = pickle.dumps(full_message)

        # Send The data to each of them
        for client in clients_to_send:
            client['client'].send('[OBJECT]'.encode())
            client['client'].send(full_message)

    def check_available_clients(self, client):
        while True:
            try:
                client.send('[Hello]'.encode())
                time.sleep(1)
            except:
                print(f'client {client} disconnected')
                break


def main():
    server = Server()


if __name__ == '__main__':
    main()
