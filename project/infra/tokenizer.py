import jwt

class Tokenizer:

    def __init__(self, secret_key):
        self.secret_key = secret_key

    def encode(self, data):
        return jwt.encode(data, self.secret_key)