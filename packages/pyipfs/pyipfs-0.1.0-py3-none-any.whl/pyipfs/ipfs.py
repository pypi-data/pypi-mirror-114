import requests
import json
import os
local = False
if local:
    from Errors import IPFSConnectionError
    from Constants import ADDFILE_ENDPINT, DOWNLOAD_PATH
else:
    from pyipfs.Errors import IPFSConnectionError
    from pyipfs.Constants import ADDFILE_ENDPINT, DOWNLOAD_PATH
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
import sys

class connection:
    def __init__(self, server = "127.0.0.1", port = "5001"):
        url = "http://{}:{}/api/v0/version/deps".format(server, port)
        try:
            response = requests.post(url)
            print("connected.")
        except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
            raise IPFSConnectionError()
            sys.exit(141)
            
    def add_files(self,filename):
        params = (
            ('chunker', 'size-262144'),
            ('quieter', 'true'),
            ('pin', 'true'),
        )
        if os.path.exists(filename):
            files = {
                'file': (os.path.basename(filename), open(filename, 'rb')),
            }
            response = requests.post('http://127.0.0.1:5001/api/v0/add', params=params, files=files).json()
            response['download'] = "{}{}".format(DOWNLOAD_PATH, response['Hash'])
            return response
        else:
            return "FILE not found."
        
        
obj = connection()
obj.add_files("/home/mahakal/Desktsop/serialized/ipfs/demo.jpg")