import requests

BASE_URL = 'https://api.bark.com'


class Client(object):
    def __init__(self, **kwargs):
        self.client_id = kwargs["client_id"]
        self.client_secret = kwargs["client_secret"]
        self.token = None

    def auth(self):

        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        url = BASE_URL + 'oauth/token'

        try:
            res = Client.http_call(method='POST', url=url, data=data)
            res.raise_for_status()
            self.token = res.json()['access_token']
            return True
        except requests.exceptions.RequestException as e:
            print(f"Failed to authenticate: {e}")
            return False

    def check_credits(self):
        if not self.token:
            print("Token is not available. Please authenticate first.")
            return None

        headers = {
            'Accept': 'application/vnd.bark.pub_v1+json',
            'Authorization': f'Bearer {self.token}'
        }
        url = BASE_URL + 'seller/credit-balance'

        try:
            res = Client.http_call(method='GET', url=url, headers=headers)
            res.raise_for_status()
            return res.json()['data']

        except requests.exceptions.RequestException as e:
            print(f"Failed to check credits: {e}")
            return None

    @staticmethod
    def http_call(method, url, headers=None, data=None):
        if method == 'GET':
            return requests.get(url=url, headers=headers, data=data)
        if method == 'POST':
            return requests.post(url=url, headers=headers, data=data)
