class Message:
    def __init__(self, text, message_code, name, receiver = None):
        self.name = name
        self.text = text
        self.message_code = message_code
        self.date = self.get_current_time()
        self.receiver = receiver

