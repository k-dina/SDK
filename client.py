import requests
from SDK.models.auth import Token
import json
import exceptions

BASE_URL = 'https://api.bark.com'
GRANT_TYPE = 'client_credentials'


class Client(object):
    def __init__(self, **kwargs):
        self.client_id = kwargs["client_id"]
        self.client_secret = kwargs["client_secret"]
        self.token = None

    def auth(self):
        data = {
            'grant_type': GRANT_TYPE,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        url = BASE_URL + 'oauth/token'

        res = self.http_call(method='POST', url=url, data=data)

        try:
            self.token = Token(res)
            return True
        except ValueError:
            self.token = None
            return False

    def list_barks(self, **kwargs):
        url = BASE_URL + 'seller/barks'
        res = self.http_call(method='GET', url=url, data=kwargs)
        return res

    def search_barks(self):
        url = BASE_URL + 'seller/barks/search'
        res = self.http_call(method='GET', url=url)
        if res['status']:
            return res['data']

    def get_bark_details(self, bark_id):
        url = BASE_URL + f'seller/bark/{bark_id}'
        res = self.http_call(method='POST', url=url)
        if res['status']:
            return res['data']

    def mark_as_not_interested(self, bark_id):
        url = BASE_URL + f'seller/bark/{bark_id}/pass'
        res = self.http_call(method='GET', url=url)
        return res['status']

    def list_recent_purchases(self):
        url = BASE_URL + 'seller/bark/purchased'
        res = self.http_call(method='GET', url=url)
        if res['status']:
            return res['data']

    def get_purchased_bark(self, bark_id):
        url = BASE_URL + f'seller/bark/purchased/{bark_id}'
        res = self.http_call(method='GET', url=url)
        if res['status']:
            return res['data']

    def purchase_bark(self, bark_id):
        url = BASE_URL + f'seller/bark/{bark_id}/purchase'
        res = self.http_call(method='POST', url=url)
        if res['status']:
            return res['buyer']

    def purchase_bark_one_click(self, bark_id):
        url = BASE_URL + f'seller/bark/{bark_id}/purchase/one-click'
        res = self.http_call(method='POST', url=url)
        if res['status']:
            return res['buyerInfo']

    def set_quote(self, bark_id, **kwargs):
        url = BASE_URL + f'seller/bark/{bark_id}/set-quote'
        res = self.http_call(method='POST', url=url, data=kwargs)
        return res['status']

    def update_bark_status(self, bark_id, status_id):
        url = BASE_URL + f'seller/bark/{bark_id}/set-status'
        res = self.http_call(method='POST', url=url, data={'status_id': status_id})
        return res['status']

    def update_bark_note(self, bark_id, note):
        url = BASE_URL + f'seller/bark/{bark_id}/set-note'
        res = self.http_call(method='POST', url=url, data={'note': note})
        return res['status']

    def check_reviews(self):
        url = BASE_URL + 'seller/reviews'
        res = self.http_call(method='GET', url=url)
        if res['status']:
            return res['data']

    def check_credits(self):
        url = BASE_URL + 'seller/credit-balance'
        res = self.http_call(method='GET', url=url)
        if res['status']:
            return res['data']

    def lookup_cities(self):
        url = BASE_URL + 'lookups/cities'
        res = self.http_call(method='GET', url=url)
        if res['status']:
            return res['data']

    def lookup_categories(self):
        url = BASE_URL + 'lookups/categories'
        res = self.http_call(method='GET', url=url)
        if res['status']:
            return res['data']

    def lookup_quote_types(self):
        url = BASE_URL + 'lookups/quote-types'
        res = self.http_call(method='GET', url=url)
        if res['status']:
            return res['data']

    def lookup_status_types(self):
        url = BASE_URL + 'lookups/status-types'
        res = self.http_call(method='GET', url=url)
        if res['status']:
            return res['data']

    def get_webhook_events(self):
        url = BASE_URL + 'webhook/events'
        res = self.http_call(method='GET', url=url, headers=False)
        if res['status']:
            return res['data']

    def subscribe_to_webhook(self, **kwargs):
        url = BASE_URL + 'webhooks'
        res = self.http_call(method='GET', url=url, data=kwargs)
        return res['id']

    def list_subscriptions(self):
        url = BASE_URL + 'webhooks'
        res = self.http_call(method='GET', url=url)
        if res['status']:
            return res['data']

    def unsubscribe_from_webhook(self, subscription_id):
        url = BASE_URL + f'webhooks/{subscription_id}'
        res = self.http_call(method='DELETE', url=url)
        return res['success']

    def http_call(self, method, url, data=None, headers=True):

        if not self.token or self.token.expires_in == 0:
            self.token = Token(self.http_call(method='POST', url=url, data=data))

        if headers:
            headers = self.get_headers()
        else:
            headers = None

        if method == 'GET':
            res = requests.get(url=url, headers=headers, data=data)
            return self.handle_response(res)
        if method == 'POST':
            res = requests.post(url=url, headers=headers, data=data)
            return self.handle_response(res)
        if method == 'DELETE':
            res = requests.delete(url=url, headers=headers, data=data)
            return self.handle_response(res)

    def get_headers(self):
        return {
            'Accept': 'application/vnd.bark.pub_v1+json',
            'Authorization': f'Bearer {self.token.access_token}'
        }

    def handle_response(self, response):
        """Validate HTTP response
                """
        status = response.status_code
        content = response.content.decode()
        if status in (301, 302, 303, 307):
            raise exceptions.Redirection(response, content)
        elif 200 <= status <= 299:
            return json.loads(content) if content else {}
        elif status == 400:
            raise exceptions.BadRequest(response, content)
        elif status == 401:
            raise exceptions.UnauthorizedAccess(response, content)
        elif status == 403:
            raise exceptions.ForbiddenAccess(response, content)
        elif status == 404:
            raise exceptions.ResourceNotFound(response, content)
        elif status == 405:
            raise exceptions.MethodNotAllowed(response, content)
        elif status == 409:
            raise exceptions.ResourceConflict(response, content)
        elif status == 410:
            raise exceptions.ResourceGone(response, content)
        elif status == 422:
            raise exceptions.ResourceInvalid(response, content)
        elif 401 <= status <= 499:
            raise exceptions.ClientError(response, content)
        elif 500 <= status <= 599:
            raise exceptions.ServerError(response, content)
        else:
            raise ConnectionError(
                response, content, "Unknown response code: #{response.code}")


