import requests
import json
from requests.auth import HTTPDigestAuth


class CASClient(object):

    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url

    @property
    def headers(self):
        return {
            "Content-Type": 'application/json',
            'Accept': 'application/json'
        }

    @property
    def auth(self):
        return HTTPDigestAuth(self.username, self.password)

    def common_request(self, method, endpoint, params={}, body={}):
        url = self.url + endpoint
        data = json.dumps(body)
        resp = getattr(requests, method)(url, headers=self.headers, auth=self.auth, params=params, data=data)

        if int(resp.status_code) != 200:
            raise Exception(resp.text)
        return json.loads(resp.text)
