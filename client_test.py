import unittest
from unittest.mock import patch
from client import Client
from SDK.models import Token
import json


class TestClient(unittest.TestCase):
    # @patch('client.requests.post')
    # def test_auth_success(self, mock_post):
    #     mock_post.return_value.json.return_value = {'access_token': 'mock_token'}
    #     client = Client(client_id='fake_client_id', client_secret='fake_client_secret')
    #     result = client.auth()
    #     self.assertEqual(client.token, 'mock_token')
    #     self.assertTrue(result)

    @patch('client.requests.get')
    def test_list_barks(self, mock_get):
        mock_get.return_value.json.return_value = {'barks': {'1': 100}}
        client = Client(client_id='fake_client_id', client_secret='fake_client_secret')
        with open('token.json') as f:
            res = json.load(f)
        client.token = Token(res)
        result = client.list_barks()
        self.assertEqual(result, {'barks': {'1': 100}})


if __name__ == '__main__':
    unittest.main()
