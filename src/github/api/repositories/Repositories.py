#!python3
#encoding
import requests
import urllib.parse
import json
class Repositories:
    def __init__(self, request_param):
        self.req = request_param

    def create(self, name, description=None, homepage=None):
        method = 'POST'
        endpoint = 'user/repos'
        params = self.req.get(method, endpoint)
        params['data'] = json.dumps({"name": name, "description": description, "homepage": homepage})
        print(params)
        r = requests.post(urllib.parse.urljoin("https://api.github.com", endpoint), **params)
        print(r.status_code)
        print(r.text)
        return json.loads(r.text)
