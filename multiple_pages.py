import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class WidgetsButtont(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        for i in range(4):layout.addWidget(QPushButton(f'Button #{i}'))

        self.setLayout(layout)

class WidgetLineEdit(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        for i in range(4):layout.addWidget(QLineEdit(f'LineEdit #{i}'))

        self.setLayout(layout)

class WidgetsRadioButtons(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        for i in range(4):layout.addWidget(QRadioButton(f'RadioButton #{i}'))

        self.setLayout(layout)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        self.stackedWidget = QStackedWidget()
        self.stackedWidget.addWidget(WidgetsButtont()) # Index 0
        self.stackedWidget.addWidget(WidgetLineEdit()) # Index 1
        self.stackedWidget.addWidget(WidgetsRadioButtons()) # Index 2

        button_previous = QPushButton('Previous')
        button_next = QPushButton('Next')
        button_next.clicked.connect(self.NextWidget)
        button_previous.clicked.connect(self.PreviousWidget)

        button_layout = QHBoxLayout()
        button_layout.addWidget(button_previous)
        button_layout.addWidget(button_next)

        main_layout.addWidget(self.stackedWidget)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.show()
    
    def NextWidget(self):
        self.stackedWidget.setCurrentIndex((self.stackedWidget.currentIndex() + 1) % 3)

    def PreviousWidget(self):
        self.stackedWidget.setCurrentIndex((self.stackedWidget.currentIndex() - 1) % 3) 



def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()