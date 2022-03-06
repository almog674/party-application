from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTime, QTimer, QSize, QThread, pyqtSignal, QMargins, QEvent
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QImage, QColor, QLinearGradient
import style
from Database import database
from spotifyClient import spotifyAPI
from play_with_images import url_to_image
import random
import time
import os
import math