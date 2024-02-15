import logging


class Token:
    def __init__(self, res):
        try:
            res = res['access_token']
            self.access_token = str(res['access_token'])
            self.type = str(res['token_type'])
            self.expires_in = int(res['expires_in'])
        except:
            raise ValueError('received data is not of expected type or contents')



