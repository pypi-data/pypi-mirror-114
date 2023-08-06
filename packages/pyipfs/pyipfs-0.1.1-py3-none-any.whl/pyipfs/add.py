
import os
import requests
local = True
if local:
    from Errors import IPFSConnectionError
    from Constants import ADDFILE_ENDPINT, DOWNLOAD_PATH
else:
    from pyipfs.Errors import IPFSConnectionError
    from pyipfs.Constants import ADDFILE_ENDPINT, DOWNLOAD_PATH
class BasicAdd:
    def __init__(self):
        pass
    def addFile(self, filename,
        quiet="false",
        quieter = "false",
        silent = "false",
        progress = "false",
        trickle = "false",
        only_hash = "false",
        wrap_with_directory = "false",
        chunker = "size-262144",
        pin = "true",
        raw_leaves = "true",
        nocopy = "false",
        fscache = "false",
        cid_version = "false",
        hash = "sha2-256",
        inline = "false",
        inline_limit = 32
    ):
        params = (
            ("quiet", quiet),
            ("quiter", quieter),
            ("silent", silent),
            ("progress" , progress),
            ("trickle", trickle),
            ("only-hash", only_hash),
            ("wrap-with-directory", wrap_with_directory),
            ("chunker", chunker),
            ("pin", pin),
            ("raw-leaves", raw_leaves),
            ("nocopy", nocopy),
            ("fscache", fscache),
            ("cid-version", 0),
            ("hash", hash),
            ("inline", inline),
            ("inline-limit", inline_limit)
        )
        #print(params)
        if os.path.exists(filename):
            files = {
                'file': (os.path.basename(filename), open(filename, 'rb')),
            }
            response = requests.post('http://127.0.0.1:5001/api/v0/add', params=params, files=files ).json()
            response['download'] = "{}{}".format(DOWNLOAD_PATH, response['Hash'])
            return response
        else:
            return "FILE not found."