import jwt

ExpiredSignatureError = jwt.ExpiredSignatureError
InvalidSignatureError = jwt.InvalidSignatureError

class Tokenizer:

    def __init__(self, secret_key):
        self.secret_key = secret_key

    def encode(self, data):
        return jwt.encode(data, self.secret_key)

    def decode(self, token, verify_signature=True):
        return jwt.decode(token, self.secret_key, options={'verify_signature':verify_signature})