import requests
import json
import os
local = False
if local:
    from Errors import IPFSConnectionError
    from Constants import ADDFILE_ENDPINT, DOWNLOAD_PATH
    from add import BasicAdd
else:
    from pyipfs.Errors import IPFSConnectionError
    from pyipfs.Constants import ADDFILE_ENDPINT, DOWNLOAD_PATH
    from pyipfs.add import BasicAdd
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
            
    def add(self,filename):
        obj = BasicAdd().addFile(filename)
        return obj
        
        
obj = connection()
n = obj.add("/home/mahakal/Desktop/serialized/demo.jpg")
print(n)