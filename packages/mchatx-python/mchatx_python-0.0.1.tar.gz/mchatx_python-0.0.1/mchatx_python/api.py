import requests
import json


class MChatX:
    def __init__(self):
        self.url = 'https://repo.mchatx.org'

    def get_room_list(self):
        r = requests.get(f'{self.url}/Room/')
        print(r.status_code)
        return r.json()

    def get_archive_list(self):
        r = requests.get(f'{self.url}/Archive/')
        return r.json()

    def download_archive(self, room_link):
        postdata = {"link": room_link}
        r = requests.post(f'{self.url}/Archive', json=postdata)
        return r.json()
    
