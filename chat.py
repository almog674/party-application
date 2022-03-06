from main_two import Main
from labrary_base import *
import threading
from gui_helper import Gui_Helper
from gui_threads import Gui_Thread_User
from reusible_widgets.message_button import Message_button


class Chat_Data:
    def __init__(self, room, DJ):
        self.room = room
        self.messages = []
        self.notefications = []
        self.channel = 'notefication'


class Chat_Channel(QWidget):
    def __init__(self, name, icon, chat_data):
        super().__init__()
        self.name = name
        self.icon = icon
        self.chat_data = chat_data
        self.UI()

    def UI(self):
        self.opacity_effect_full = QGraphicsOpacityEffect()
        self.opacity_effect_full.setOpacity(1)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.3)

        self.setStyleSheet('''
            background-color: transparent;
        ''')
        self.installEventFilter(self)
        self.setFixedHeight(60)
        self.setFixedWidth(180)
        self.setCursor(Qt.PointingHandCursor)

        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.main_layout.setSpacing(0)

        self.text = QLabel(self.name)
        self.text.setStyleSheet('''color: white; font-size: 18px;''')
        self.text.setFixedWidth(160)
        self.text.setFixedHeight(60)
        self.icon = Gui_Helper.make_icon(
            self=self, url=self.icon, width=20, height=20, color='white')
        self.icon.setFixedWidth(40)
        self.icon.setStyleSheet(''' ''')

        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.icon)
        self.main_layout.addWidget(self.text, alignment=Qt.AlignCenter)
        self.main_layout.addStretch(1)

        self.setLayout(self.main_layout)
        self.show()

    def eventFilter(self, obj, event):
        if obj == self and event.type() == 10:
            self.onHovered()
        elif obj == self and event.type() == 11:
            self.offHovered()
        return super().eventFilter(obj, event)
        # return super(Widget, self).eventFilter(obj, event)

    def onHovered(self):
        self.text.setStyleSheet(
            '''color: white; font-size: 18px; background-color: rgb(255, 0, 142);''')
        # self.setGraphicsEffect(self.opacity_effect)
        self.setStyleSheet('''
            background-color: rgb(255, 0, 142);
        ''')

    def offHovered(self):
        self.text.setStyleSheet('''color: white; font-size: 18px''')
        # self.setGraphicsEffect(self.opacity_effect_full)
        self.setStyleSheet('''
            background-color: transparent;
        ''')


class Chat_UI(QWidget):
    def __init__(self, chat, user):
        super().__init__()
        self.chat_data = chat
        self.user = user
        self.name = self.user.name
        self.old_messsages = []
        self.old_notefications = []
        self.message = self.old_channel = self.layout = None
        self.user.gui_thread.make_chat_message.connect(
            lambda: self.build_single_message(self.message, self.old_channel, self.layout))
        self.UI()

    def UI(self):
        self.setWindowTitle('Chat Application')
        self.setFixedSize(750, 500)

        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.main_layout.setSpacing(0)

        self.make_widgets()
        self.make_layouts()

        self.setLayout(self.main_layout)

    def create_message_chat(self, message_name, message_text, message_date, sender):
        message_container = QGroupBox()
        message_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        message_container.setMinimumWidth(100)
        message_container = Gui_Helper.add_shadow(
            self=self, widget=message_container, y=3, x=3, blur=10)
        if sender == True:
            message_container.setStyleSheet(style.chat_message_container_two())
            message_container.setAlignment(Qt.AlignRight)
        else:
            message_container.setStyleSheet(style.chat_message_container_one())
            message_container.setAlignment(Qt.AlignLeft)
        message_container, container_box = self.create_message_ui(
            message_container, message_name, message_text, message_date)
        return message_container, container_box

    def create_message_ui(self, message_container, message_name, message_text, message_date):
        container, container_box = Gui_Helper.make_layout_full(
            message_container, style_function=style.chat_message_container_two)

        message_container.text = QLabel(message_text)
        message_container.text.setStyleSheet('''
            font-size: 12px;
            margin-left: 7px;
            margin-right: 7px;
            margin-top: 3px;
            margin-bottom: 3px;
        ''')

        message_container.name = QLabel(message_name)
        message_container.name.setStyleSheet('''
            margin-right: 7px;
            margin-top: 7px;
            font-size: 10px;
            color: red;
        ''')
        message_container.name.setAlignment(Qt.AlignRight)
        # message_container.set_size_policy(message_container.name)

        message_container.date = QLabel(message_date)
        message_container.date.setStyleSheet('''
            font-size: 10px;
            margin-left: 7px;
            margin-bottom: 5px;
            color: #aaa; 
        ''')
        message_container.date.setAlignment(Qt.AlignLeft)
        # message_container.set_size_policy(message_container.date)

        container.addWidget(message_container.name, alignment=Qt.AlignRight)
        container.addWidget(message_container.text)
        container.addWidget(message_container.date, alignment=Qt.AlignLeft)

        message_container.setLayout(container)
        return message_container, container_box

    def update_chat_data(self, chat_data):
        self.chat_data = chat_data

    def send_message(self, event):
        if self.stack_messages.currentIndex() == 1:
            Gui_Helper.make_message_box(
                self=self, text="You can't write messaegs in the notifications room")
            return
        if len(self.message_input.text()) == 0:
            return
        self.user.send_message()
        self.message_input.setText('')

    def build_message_text(self):
        if self.stack_messages.currentIndex() == 0:
            channel = self.chat_data.messages
            self.old_channel = self.old_messsages
            self.layout = self.message_broadcast_channel
        else:
            channel = self.chat_data.notefications
            self.old_channel = self.old_notefications
            self.layout = self.message_notefication_channel
        for message in channel:
            self.message = message
            self.user.gui_thread.make_chat_message_func()

    def build_single_message(self, message, old_channel, layout):
        if message not in old_channel:
            message_name = message['message_name']
            message_text = message['message_text']
            message_date = message['message_date']
            old_channel.append(message)
            if self.name == message_name:
                message, message_box = self.create_message_chat(
                    message_name, message_text, message_date, True)
            else:
                message, message_box = self.create_message_chat(
                    message_name, message_text, message_date, False)
            layout.addRow(message)

    def make_simple_gradient(self, color_one, color_two, start_point=(0, 0), end_point=(0, 0)):
        grad = QLinearGradient()
        grad.setColorAt(0.0, QColor(color_one))
        grad.setColorAt(1.0, QColor(color_two))
        grad.setStart(start_point[0], start_point[1])
        grad.setFinalStop(end_point[0], end_point[1])
        return grad

    def make_message_section(self):
        self.stack_messages = QStackedWidget()
        self.message_broadcast_channel, self.message_broadcast_channel_box = self.make_message_layouts()
        self.message_notefication_channel, self.message_notefication_channel_box = self.make_message_layouts()
        self.message_broadcast_channel_box.setStyleSheet(
            style.chat_main_right_scroll())
        self.message_notefication_channel_box.setStyleSheet(
            style.chat_main_right_scroll())
        self.stack_messages.addWidget(self.message_broadcast_channel_box)
        self.stack_messages.addWidget(self.message_notefication_channel_box)

    def make_message_layouts(self):
        main_right_layout, main_right_layout_box = Gui_Helper.make_layout_full(
            self, style_function=style.chat_main_right_layout, directon=2)
        main_scroll = Gui_Helper.make_layout_scrollable(
            self=self, layout=main_right_layout_box, vertical=True, height=340)
        main_scroll.verticalScrollBar().setStyleSheet(style.chat_main_scroll())
        return (main_right_layout, main_scroll)

    def go_to_channel(self, channel, channel_name):
        self.stack_messages.setCurrentIndex(channel)
        self.room_title.setText(channel_name)
        self.build_message_text()

    def make_widgets(self):
        self.background = QGroupBox()
        self.background.setFixedSize(750, 500)
        self.background.setStyleSheet(style.chat_main())

        self.main_content, self.main_content_box = Gui_Helper.make_layout_full(
            self, style_function=style.empty, directon=1)

        ### Left Side Widgets ###
        self.profile_picture, profile_pixmap = Gui_Helper.make_picture(
            self, url='player_images\picture-profile.jpg', width=70, height=70)
        self.profile_picture.setStyleSheet(style.chat_profile_picture())
        self.profile_name = QLabel(self.name)
        self.profile_name.setStyleSheet(style.chat_profile_name())

        self.broadcast_channel = Chat_Channel(
            'Room Channel', 'player_icons\\users-icon.svg', self.chat_data)
        self.notificationa = Chat_Channel(
            'Notifications', 'player_icons\\bell-icon.svg', self.chat_data)
        self.broadcast_channel.mousePressEvent = lambda fucntion: self.go_to_channel(
            0, 'Room Channel')
        self.notificationa.mousePressEvent = lambda function: self.go_to_channel(
            1, 'Notifications')

        ### Right Side Widgets ###
        self.room_title = QLabel('Broadcast Channel')
        self.room_title.setStyleSheet(style.chat_room_title())

        self.message_input = QLineEdit()
        self.message_input.setStyleSheet(style.chat_message_input())
        self.message_input.setFixedHeight(35)
        self.message_input.setMaxLength(200)
        self.message_input.setPlaceholderText('Write a message here...')
        self.message_input.setFixedWidth(400)

        self.message_button_container = Message_button(
            'SEND', 'player_icons\\arrow-right-icon.svg', self.send_message)

    def make_layouts(self):
        self.stack_widget = QStackedWidget()
        bottom_widget_layout = self.stack_widget.layout()
        bottom_widget_layout.setStackingMode(QStackedLayout.StackAll)

        left_side_width = 180
        self.left_side, self.left_side_box = Gui_Helper.make_layout_full(
            self, style_function=style.chat_left_side, width=left_side_width)
        self.right_side, self.right_side_box = Gui_Helper.make_layout_full(
            self, style_function=style.chat_right_side, width=(750 - left_side_width))

        ### Making Left Side ###
        self.profile_section, self.profile_section_box = Gui_Helper.make_layout_full(
            self, style_function=style.empty, height=125)
        self.profile_section.addStretch(2)
        self.profile_section.addWidget(
            self.profile_picture, alignment=Qt.AlignHCenter)
        self.profile_section.addStretch(1)
        self.profile_section.addWidget(
            self.profile_name, alignment=Qt.AlignHCenter)
        self.profile_section.addStretch(1)

        ### Making Right Side ###
        self.top_right_layout, self.top_right_layout_box = Gui_Helper.make_layout_full(
            self, style_function=style.chat_top_right_layout, height=75)
        self.make_message_section()
        self.bottom_right_layout, self.bottom_right_layout_box = Gui_Helper.make_layout_full(
            self, style_function=style.chat_bottom_right_layout, height=75, directon=1)

        # Adding The Nested Layouts
        self.main_layout.addWidget(self.stack_widget)

        self.stack_widget.addWidget(self.main_content_box)
        self.stack_widget.addWidget(self.background)

        self.main_content.addWidget(self.left_side_box, alignment=Qt.AlignLeft)
        self.main_content.addWidget(
            self.right_side_box, alignment=Qt.AlignRight)

        self.left_side.addWidget(
            self.profile_section_box, alignment=Qt.AlignTop)
        self.left_side.addWidget(self.broadcast_channel, alignment=Qt.AlignTop)
        self.left_side.addWidget(self.notificationa, alignment=Qt.AlignTop)
        self.left_side.addStretch()

        self.right_side.addWidget(
            self.top_right_layout_box, alignment=Qt.AlignTop)
        self.top_right_layout.addWidget(
            self.room_title, alignment=Qt.AlignCenter)
        self.right_side.addWidget(self.stack_messages)
        self.right_side.addWidget(
            self.bottom_right_layout_box, alignment=Qt.AlignBottom)
        self.bottom_right_layout.addWidget(self.message_input)
        self.bottom_right_layout.addWidget(self.message_button_container)
