import unittest
import requests
from unittest.mock import patch
from client import Client


class TestClient(unittest.TestCase):
    @patch('client.requests.post')
    def test_auth_success(self, mock_post):
        mock_post.return_value.json.return_value = {'access_token': 'mock_token'}
        client = Client(client_id='fake_client_id', client_secret='fake_client_secret')
        result = client.auth()
        self.assertEqual(client.token, 'mock_token')
        self.assertTrue(result)

    @patch('client.requests.post')
    def test_auth_failure(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException('Mocked exception')
        client = Client(client_id='fake_client_id', client_secret='fake_client_secret')
        result = client.auth()
        self.assertIsNone(client.token)
        self.assertFalse(result)

    @patch('client.requests.get')
    def test_check_credits(self, mock_get):
        mock_get.return_value.json.return_value = {'data': {'credits': 100}}
        client = Client(client_id='fake_client_id', client_secret='fake_client_secret')
        client.token = 'mock_token'
        result = client.check_credits()
        self.assertEqual(result, {'credits': 100})


if __name__ == '__main__':
    unittest.main()
