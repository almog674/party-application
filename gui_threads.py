from main_two import *

class Gui_Thread(QThread):
    update_waiting_page = pyqtSignal(bool)
    update_party_page = pyqtSignal(bool)
    delete_waiting_user_grid = pyqtSignal(bool)
    delete_DJ_users_list = pyqtSignal(bool)
    make_message_box = pyqtSignal(bool)
    make_chat_message = pyqtSignal(bool)

    def make_chat_message_func(self):
        self.make_chat_message.emit(True)

    def make_message_box_func(self):
        self.make_message_box.emit(True)

    def delete_DJ_users_list_func(self):
        self.delete_DJ_users_list.emit(True)

    def update_waiting_page_func(self):
        self.update_waiting_page.emit(True)

    def delete_waiting_grid(self):
        self.delete_waiting_user_grid.emit(True)

    def update_party_page_func(self):
        self.update_party_page.emit(True)


class Gui_Thread_User(Gui_Thread):
    room_value = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()

    def go_to_page_0(self):
        self.room_value.emit((0 ,(150, 100, 400, 250), "Join Party"))

    def go_to_page_1(self):
        self.room_value.emit((1 ,(150, 100, 950, 675), "Waiting Room"))

    def go_to_page_2(self):
        self.room_value.emit((2 ,(150, 100, 950, 675), "User Party"))

class Gui_Thread_DJ(Gui_Thread):
    room_value = pyqtSignal(tuple)
    def __init__(self):
        super().__init__()

    def go_to_page_0(self):
        self.room_value.emit((0 ,(150, 100, 950, 675), "DJ Party"))
        
    def go_to_page_1(self):
        self.room_value.emit((1 ,(150, 100, 950, 675), "DJ Room"))



    
