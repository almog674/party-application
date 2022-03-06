import pymongo
import cv2
import os
from pygame import mixer


### Initialize Mixer ###
song_mixer = mixer
song_mixer.init()

### Read the data ###
image = open('im yours.mp3', 'rb')
data_array = []
for line in image:
    data_array.append(line)

### connect to the database ###
myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient["authenticationDB"]
songs_col = mydb['audio']


### Write the data to the db ###
# songs_col.insert_one({'name': 'im yours', 'data' : data_array})


### Extract the data from the database ###
data_from_db = songs_col.find_one({'name': 'im yours'})

### clean the data ###
picture_data_str = data_from_db["data"]
new_picture = open('new_song.mp3', 'wb')
for line in picture_data_str:
    new_picture.write(line)

# data_1 = open('im yours.mp3', 'rb')
# data_2 = open('new song.mp3', 'rb')
# print(data_1 == data_2)
### Open the file ###
name = 'new song.mp3'
directory = os.path.dirname(os.path.realpath(name))
full = directory + '\\' + name

song_mixer.music.load(full)
song_mixer.music.set_volume(0.7)
song_mixer.music.play()


while True:
    pass