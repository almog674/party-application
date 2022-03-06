import pymongo


class database:
    def __init__(self):
        # Create a Client
        self.myclient = pymongo.MongoClient('mongodb://localhost:27017/')
        # Create the database
        self.mydb = self.myclient["authenticationDB"]
        # Create the collections
        self.users_col = self.mydb['users']
        self.songs_col = self.mydb['songs']

        # self.delete_all_songs()
        # self.delete_all_users()

    #################### Auth #####################

    def authenticate(self, username, password):
        ### Authenticate user to the app ###
        if (username == '') or (password == ''):
            return 'You forgot one field empty'

        exist = self.search_if_user('username', username)
        if exist == False:
            return "User dosn't existing"

        exist = self.search_if_user('username', username, 'password', password)
        if exist == False:
            return "Password is wrong"

        return 'authenticated succesfuly'

    def search_if_user(self, parameter, value, parameter_2=False, value_2=False, parameter_3=False, value_3=False):
        ### Checking if the user is existing in the database ###
        if parameter_3 != False:
            my_query = {parameter: value,
                        parameter_2: value_2, parameter_3: value_3}
        elif parameter_2 != False:
            my_query = {parameter: value, parameter_2: value_2}
        else:
            my_query = {parameter: value}
        if self.users_col.count_documents(my_query) == 0:
            return False
        return True

    def print_all_database(self):
        ### Printing all the users ###
        my_query = {}
        result = self.users_col.find(my_query)
        for x in result:
            print('Username: ' + x['username'] + ' Password: ' +
                  x['password'] + ' Liked Songs: ' + str(x['playlist']))

    def delete_all_users(self):
        my_query = {}
        result = self.users_col.delete_many(my_query)
        print('deleted all users!!')

    def add_user(self, username, email, password):
        user = {'username': username, 'email': email,
                'password': password, 'playlist': []}
        self.users_col.insert_one(user)

    def create_user(self, username, email, password, prepassword):
        # Checking the Validation of those values
        username_valid = self.check_valid_username(username)
        email_valid = self.check_valid_email(email)
        password_valid = self.check_valid_password(username, password)
        prepassword_valid = self.check_valid_prepassword(password, prepassword)

        # Handle diffrent option of invalid syntax
        valid = self.handle_create_user_validation(
            username_valid, email_valid, password_valid, prepassword_valid)
        if valid != '100':
            return valid
        self.add_user(username, email, password)
        return 'user created successfuly!!'

    def handle_create_user_validation(self, username_valid, email_valid, password_valid, prepassword_valid):
        ### If one or more fields is invalid, return where is the problem ###
        if (username_valid == False) or (email_valid == False) or (password_valid == False) or (prepassword_valid == False):
            if (username_valid == False):
                return ('Username is invalid')
            elif (email_valid == False):
                return ('Email is invalid')
            elif (password_valid == False):
                return ('Password is invalid')
            else:
                return ('Password Validation is invalid')
        return '100'

    def check_valid_username(self, username):
        ### username rules ###
        # 1. not empty or bigger then 13 letters
        # 2. not containing one or more symbols
        # 3. not already existing
        symbols = ['[', ']', '@', '#', '!', '~', '&', '$']
        if (len(username) == 0) or (len(username) > 13):
            return False
        exist = self.search_if_user('username', username)
        for symbol in symbols:
            if symbol in username:
                return False
        if exist == True:
            return False
        return True

    def check_valid_email(self, email):
        ### email rules ###
        # 1. not less then 5 letters or bigger then 30 letters
        # 2. containing the symbol "@"
        # 3. not already existing
        if (len(email) < 5) or (len(email) > 30):
            return False
        elif '@' not in email:
            return False
        exist = self.search_if_user('email', email)
        if exist == True:
            return False
        return True

    def check_valid_password(self, username, password):
        ### password rules ###
        # 1. not less then 5 letters or bigger then 13 letters
        # 2. not identical to the useename
        if (len(password) < 5) or (len(password) > 13):
            return False
        elif username == password:
            return False
        return True

    def check_valid_prepassword(self, password, prepassword):
        ### password validation rules ###
        # 1. Identical to the password
        if password != prepassword:
            return False
        return True

    def get_user_values(self, usename):
        my_query = {'username': usename}
        user = self.users_col.find(my_query)
        for x in user:
            return x['password'], x['email'], x['playlist']

    #################### Auth #####################

    #################### Songs #####################

    def check_if_song_exist(self, song_name):
        my_query = {'song_name': song_name}
        if self.songs_col.count_documents(my_query) > 0:
            return True
        return False

    def add_song(self, song_name, audio, user_name, duration, artist='unknown', background_url='', file_format='.mp3'):
        # Insert one song from the player to the database
        exist = self.check_if_song_exist(song_name)
        if exist == True:
            return 'the song is already in database'
        if artist == None:
            artist = 'unknown'
        my_song = {
            'song_name': song_name,
            'user_name': user_name,
            'duration': duration,
            'artist': artist,
            'background_url': background_url,
            'file_format': file_format,
            'audio': audio
        }
        self.songs_col.insert_one(my_song)

    def search_song(self, song_name, artist_name):
        if song_name == '':
            return 'error'
        if artist_name == '':
            artist_name = None
        full_data = self.get_song_data(song_name, artist_name)
        return full_data

    def like_song(self, song_name, user_name):
        my_query = {'username': user_name}
        result = self.users_col.find_one(my_query)

        if song_name not in result['playlist']:
            new_list = result['playlist']
            new_list.append(song_name)
            print('adding the song to the database')
        else:
            new_list = result['playlist']
            new_list.remove(song_name)
            print('deleting the song to the database')

        new_values = {'$set': {'playlist': new_list}}
        self.users_col.update_one(my_query, new_values)

    def get_liked_song(self, user_name):
        my_query = {'username': user_name}
        result = self.users_col.find_one(my_query)

        if not result:
            return
        liked_list = result['playlist']
        return liked_list

    def delete_all_songs(self):
        # Delete all the songs
        my_query = {}
        self.songs_col.delete_many(my_query)
        print('deleted all the songs')

    def get_song_data(self, song_name, artist_name=None):
        if artist_name == None:
            my_query = {'song_name': song_name}
        else:
            my_query = {'song_name': song_name, 'artist': artist_name}
        return self.songs_col.find_one(my_query)

    def print_all_songs(self):
        ### Printing all the users ###
        my_query = {}
        result = self.songs_col.find(my_query)
        print('asd')
        for x in result:
            print('Song name: ' + x['song_name'] + 'Artist: ' + x['artist'])

    #################### Songs #####################


# base = database()
# base.create_user('almog999', 'almogmaimon674@gmail.com',
#                  'almog674', 'almog674')
