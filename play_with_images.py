import cv2
import urllib.request
import numpy as np

song_data = {'height': 640, 'url': 'https://i.scdn.co/image/ab67616d0000b27377cbce79612c3a9664234883', 'width': 640}

class url_to_image():
    def convert_url(self, url):
        print(url)
        resp = urllib.request.urlopen(url)
        # image = np.asarray(bytearray(resp.read()), dtype = 'uint8')
        # image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return resp

    def show_image(self, image):
        cv2.imshow('almog', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# almog = url_to_image()
# image = almog.convert_url(song_data['url'])