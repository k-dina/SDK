import requests
import datetime
import json
from pydantic import ValidationError

from SDK.models import Token, SimpleResponse
from util import datetime_to_sec, get_url
from config import GRANT_TYPE


class Client(object):
    def __init__(self, **kwargs):
        self.client_id = kwargs["client_id"]
        self.client_secret = kwargs["client_secret"]
        self.token = None

    # аутентификация
    def auth(self) -> (bool, str):
        data = {
            'grant_type': GRANT_TYPE,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        url = get_url('auth')
        res = requests.post(url=url, headers=self.get_headers(), data=data)
        if res.status_code == 200:
            # куда еще поместить парсинг? у меня так и не получилось придумать.
            # тут model_validate_json парсит в момент складывания в модель
            try:
                self.token = Token.model_validate_json(res.content)
                self.token.requested_at = datetime.datetime.now()
                return True, 'ok'
            except ValidationError:
                return False, 'content not of expected type'
        return False, res.content.decode()

    # проверяет, жив ли еще токен и обновляет его, если нет
    def validate_token(self):
        delta = datetime_to_sec(datetime.datetime.now() - self.token.requested_at)
        if delta > self.token.expires_in:
            self.auth()

    def check_credits(self):
        self.validate_token()
        url = get_url('check_credits')
        res = SimpleResponse.model_validate(self.http_call(method='GET', url=url))
        if res.status:
            return res.body
        return res.status

    def http_call(self, method, url, data=None, headers=True):
        if headers:
            headers = self.get_headers()
        else:
            headers = None

        if method == 'GET':
            return json.loads(requests.get(url=url, headers=headers, data=data).content)
        if method == 'POST':
            return json.loads(requests.post(url=url, headers=headers, data=data).content)
        if method == 'DELETE':
            return json.loads(requests.delete(url=url, headers=headers, data=data).content)

    def get_headers(self):
        return {
            'Accept': 'application/vnd.bark.pub_v1+json',
            'Authorization': f'Bearer {self.token.access_token}'
        }
