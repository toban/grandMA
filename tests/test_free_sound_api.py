import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from freesound_api import *
import unittest
from mock import MagicMock
from dotenv import load_dotenv
import simpleaudio as sa

load_dotenv()

API_KEY = os.getenv('FREESOUND_API_KEY')
ACCESS_TOKEN = os.getenv('FREESOUND_ACCESS_TOKEN')
CLIENT_ID = os.getenv('FREESOUND_CLIENT_ID')
AUTH_KEY = os.getenv('FREESOUND_AUTH_CODE')

class TestFresoundAPI(unittest.TestCase):

    def test_upper(self):
        api = FreesoundAPI(API_KEY, ACCESS_TOKEN)
        #api.method = MagicMock(return_value=3)
        #api.method(3, 4, 5, key='value')
        #api.method.assert_called_with(3, 4, 5, key='value')

        response = api.get_audio('lazer')
        #print(dir(response))
        json = response.json()
        for i in json['results']:
            print(i)
            sound = api.get_sound(i['id']).json()
            
            preview = api.get_preview(sound)
            print(preview)

            filename = api.download_sound(sound, preview)

            wave_obj = sa.WaveObject.from_wave_file(filename)
            play_obj = wave_obj.play()
            play_obj.wait_done()
            
            break
        self.assertEqual('foo'.upper(), 'FOO')

'''
    def test_OAuth(self):

        codeUrl = "https://freesound.org/apiv2/oauth2/authorize/?client_id=" + CLIENT_ID + "&response_type=code"
        print(codeUrl)
        
        params = {
            'client_id:': CLIENT_ID,
            'client_secret': API_KEY,
            'grant_type': 'authorization_code',
            'code': AUTH_KEY
        }
        print(params)
        resp = requests.post('https://freesound.org/apiv2/oauth2/access_token/', params)

        print(resp.json())
'''

if __name__ == '__main__':
    unittest.main()