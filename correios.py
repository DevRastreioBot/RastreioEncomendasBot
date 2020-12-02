import json

import requests

base = "https://api.linketrack.com/track/json"


class Correios:

    def __init__(self, user, token):
        self.user = user
        self.token = token

    def rastrear(self, codigo):
        response = requests.request("GET", f'{base}?user={self.user}&token={self.token}&codigo={codigo}', headers={},
                                    data={})

        try:
            if response.status_code == 200:
                return json.loads(response.text.encode('utf8'))
            else:
                return None
        except:
            return None
