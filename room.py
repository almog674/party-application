import random
from chat import Chat_Data

class Room:
    def __init__(self, DJ, name = 'a'):
        self.name = name
        self.code = self.get_room_code()
        self.DJ = DJ
        self.chat = Chat_Data(self, self.DJ)
        self.users = []
        self.like_users = []
        self.hate_users = []
        self.is_active = False
        

    def __str__(self):
        return f'Room name: {self.name}\nRoom code: {self.code}\nRoom DJ: {self.DJ}\nRoom users: {self.users}\nRoom active: {self.is_active}'

    def get_room_code(self):
        code = ''
        for i in range(8):
            number = random.randint(0, 1)
            code += str(number)
        return code