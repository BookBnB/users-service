from project.db import db
from project.models.server import Server
from secrets import token_hex

class ServerService:
    def create_server(self, values_dict):
        values_dict['token'] = token_hex(24)
        server = Server(**values_dict)
        db.session.add(server)
        db.session.commit()

        return server

    def get_all(self):
        return Server.query.all()

    def find_by_token(self, token):
        return Server.query.filter_by(token=token).first()

    def find_by_name(self, name):
        return Server.query.filter_by(nombre=name).first()

    def save(self, server):
        db.session.commit()