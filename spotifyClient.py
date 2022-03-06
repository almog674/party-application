import requests
import base64
import datetime
from urllib.parse import urlencode

client_id = '9c8a8a4cfe9c492a86eced46e6ac829b'
client_secret = '6d71b04b746c4ca6bb548f79a13bfb26'

class spotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id, client_secret, *args):
        super().__init__()
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_creds(self):
        client_id = self.client_id
        client_secret = self.client_secret
        if (client_id == None) or (client_secret == None):
            raise Exception('You must set client_id and client_secret')
        client_creds = f'{client_id}:{client_secret}'
        client_creds_64 = base64.b64encode(client_creds.encode())
        return client_creds_64.decode()


    def get_token_header(self):
        client_creds_64 = self.get_client_creds()
        token_header = {
            'Authorization': f"basic {client_creds_64}"
        }
        return token_header

    def get_token_data(self):
        token_data = {
            'grant_type': 'client_credentials'
        }
        return token_data

    def extract_access_token(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_header = self.get_token_header()
        ### Making a post request with python, important to other project as well ###
        r = requests.post(token_url, data = token_data, headers = token_header)
        valid_code = r.status_code in range(200,299)

        if valid_code:
            data = r.json()
            now = datetime.datetime.now()
            self.access_token = data['access_token']
            expires_in = data['expires_in'] # seconds
            self.access_token_expires = now + datetime.timedelta(seconds = expires_in)
            self.access_token_did_expire = (self.access_token_expires < now)
            return True
        return False

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.extract_access_token()
            return self.get_access_token()
        elif token == None:
            self.extract_access_token()
            return self.get_access_token()
        return token

    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
        'Authorization' : f'Bearer {access_token}'
        }
        return headers

    def get_resource(self, lookup_id, resource_type = 'albums', version = 'v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers = headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_artist(self, _id):
        return self.get_resource(_id, resource_type = 'artists')

    def get_album(self, _id):
        return self.get_resource(_id, resource_type = 'albums')

    def seperate_songs(self, results, option_number):
        results_split = results['tracks']['items']
        if option_number == len(results_split):
            return '0'
        results_choosen = results_split[option_number]
        return results_choosen

    def get_artist_id(self, song):
        pass

    def get_songs_duraton(self, song):
        duration_ms = song['duration_ms']
        duration_sec = duration_ms / 1000
        min, sec = divmod(duration_sec, 60)
        sec = round(sec)
        sec = str(sec)
        sec = sec.zfill(2)
        duration = f'{int(min)}:{sec}'
        return duration

    def get_background_url(self, song):
        results_album = song['album']
        result_images = results_album['images']
        result_backgrounds = result_images[0]
        results_url = result_backgrounds['url']
        return results_url

    def get_song_artist(self, song):
        results_album = song['album']
        result_artists = results_album['artists']
        atrist_name = result_artists[0]['name']
        return atrist_name

    def get_song_album(self, song):
        return 1

    def clear_song_data(self, song, expected_artist = None):
        background_url = self.get_background_url(song)
        song_duration = self.get_songs_duraton(song)
        artist_name = self.get_song_artist(song)
        if (expected_artist != None) and (expected_artist.lower() != artist_name.lower()):
            code = '1'
        else:
            code = '0'
        song_name = song['name']
        full_data = {
            'code': code,
            'song_name' : song_name,
            'artist_name' : artist_name,
            'song_duration' : song_duration,
            'background_url' : background_url
        }
        return full_data

    def get_artist_genres(self, artist):
        genres = artist['genres']
        return genres

    def get_artist_image(self, artist):
        image_list = artist['images']
        image = image_list[0]
        image_url = image['url']
        return image_url

    def clear_artist_data(self, artist):
        artist = artist['artists']
        items = artist['items'][0]
        genres = self.get_artist_genres(items)
        image_url = self.get_artist_image(items)
        full_data = {'genres' : genres, 'image_url' : image_url}
        return full_data

    def base_search(self, query_params, search_type = 'artists', option_number = None, expected_artist = None):
        headers = self.get_resource_header()
        endpoint = 'https://api.spotify.com/v1/search'
        # Gets the data of songs
        lookup_url = f'{endpoint}?{query_params}'
        r = requests.get(lookup_url, headers = headers)
        if r.status_code not in range(200, 299):
            return {}
        if (option_number != None) and (type(option_number) == int) and (search_type == 'track'):
            result = self.seperate_songs(r.json(), option_number)
            if result == '0':
                return 'Error: song didnt found'
            clear_song_data = self.clear_song_data(result, expected_artist)
            # print(clear_song_data)
            if clear_song_data['code'] == '1':
                return self.base_search(query_params, search_type, option_number = (option_number + 1), expected_artist = expected_artist)
            return clear_song_data
        if search_type == 'artist':
            clear_artist_data = self.clear_artist_data(r.json())

            return clear_artist_data
        return r.json()

    def search(self, query = None, operator = None, operator_query = None, search_type = 'artist', option_number = None, expected_artist = None):
        if query == None:
            raise Exception('A query is required')
        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k, v in query.items()])
        if (operator != None) and (operator_query != None):
            if (operator.lower() == 'or') or (operator.lower() == 'not'):
                operator = operator.upper()
                if isinstance(operator_query, str):
                    query = f'{query} {operator} {operator_query}'
        query_params = urlencode({'q': query, 'type': search_type.lower()})
        resault = self.base_search(query_params, search_type, option_number = option_number, expected_artist = expected_artist)
        return resault



### Expected Values ###
# 1. artist name

client = spotifyAPI(client_id, client_secret)
# answer = client.search(query = 'Believer', search_type = 'track', option_number = 0, expected_artist = 'Imagine Dragons')
# answer = client.search(query = 'avicii')
# answer = client.search(query = 'Time', search_type = 'track', option_number = 0, expected_artist = 'hans zimmer')
# answer = client.search(query = 'איך אפשר שלא להתאהב בך', search_type = 'track', option_number = 0)
# answer = client.search(query = 'יאנג בויז 3', search_type = 'track', option_number = 0)
# answer = client.search(query = 'califotnia dreamen', search_type = 'track', option_number = 0)
# get_artist = client.search(query = 'avicii')
# print('*')
# print('*')
# print('*') 
# print('*')
# print('*')
# print('*')
# print(client.get_artist('1vCWHaC5f2uS3yhpwWbIA6'))