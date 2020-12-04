import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv('SECRET_KEY')

    # expresado en segundos, default 24hs
    SESSION_TOKEN_DURATION = int(os.getenv('SESSION_TOKEN_DURATION') or "86400")
