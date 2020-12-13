from google.oauth2 import id_token
from google.auth.transport import requests


class TokenError(ValueError):
    pass


class OAuth:

    def __init__(self, client_id):
        self.client_id = client_id

    def verify(self, token):
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), self.client_id)
            print(idinfo, flush=True)
            return idinfo
        except ValueError as e:
            raise TokenError(str(e))
