import os
from os import listdir
from os.path import isfile, join
import requests
from os.path import exists


class FreesoundAPI():
    def __init__(self, api_key, access_token):
        self.api_key = api_key
        self.access_token = access_token
        self.host = "https://freesound.org/apiv2"

    def get_audio(self, query):
        response = requests.get( self.host + '/search/text/?query='+query+'&token=' + self.api_key)
        return response
    
    def download_sound(self, sound, preview):

        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        url = sound['download']
        filename = 'downloads/' + str(sound['id']) + "." + sound['type']
        
        if preview:
            url = preview
            filename = 'downloads/' + str(sound['id']) + "_preview." + sound['type']
        
        headers = {
            'Authorization': "Bearer " + self.access_token
        }

        if not exists(filename):
            with requests.get(url, stream=True, headers=headers) as r:
                r.raise_for_status()
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): 
                        f.write(chunk)
        
        return filename
        

    def get_preview(self, sound):
        if 'preview-lq-ogg' in sound['previews']:
            return sound['previews']['preview-lq-ogg']
        else:
            return None

    def get_sound(self, sound_id):
        response = requests.get( self.host + '/sounds/' + str(sound_id) + '/?token=' + self.api_key)
        return response