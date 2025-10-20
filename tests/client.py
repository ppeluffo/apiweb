#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python
"""
Genero datos simulando ser un PLC.
"""

import requests
import pprint

class Frames:

    def __init__(self):
        self.url = 'http://127.0.0.1:5500/apiweb'


    def help(self):
        r = requests.get(url=self.url + '/help', timeout=10)
        print(f"HELP TEST(GET): {r.status_code}") 
        if r.status_code == 200:
            d_rsp = r.json()
            print('HELP RESPONSE:')
            pprint.pprint(d_rsp)

    def ping(self):
        r = requests.get(url=self.url + '/ping', timeout=10)
        print(f"PING TEST(GET): {r.status_code}") 
        if r.status_code == 200:
            d_rsp = r.json()
            print('TEST RESPONSE:')
            pprint.pprint(d_rsp)


    """
    def config(self, id='PLCTEST'):
        params = {'ID':id, 'TYPE': 'PLCV2', 'VER':'1.0.0'}
        data = b'C\xfe\xb1'
        r = requests.post(url=self.url, params=params, data=data, timeout=10)
        print(f"PING TEST(POST): {r.status_code}")


    def ping(self,id='PLCTEST'):
        params = {'ID':id, 'TYPE': 'PLCV2', 'VER':'1.0.0'}
        data = b'P\xe6\xcd'
        r = requests.post(url=self.url, params=params, data=data, timeout=10)
        print(f"PING TEST(POST): {r.status_code}")
    """





if __name__ == '__main__':

    frames = Frames()

    frames.help()
    #frames.ping()
    #frames.config()