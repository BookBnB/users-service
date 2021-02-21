from project.db import db
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import re

from project.models.role import ROLES


class Server(db.Model):
    __tablename__ = "servers"

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True)
    nombre = db.Column(db.String(256), nullable=False)
    token = db.Column(db.String(256), nullable=False)

    def __init__(self, **kwargs):
        self.assert_key(kwargs, 'nombre')
        self.assert_key(kwargs, 'token')

        self.nombre = kwargs['nombre']
        self.token = kwargs['token']

    def assert_key(self, values_dict, key):
        if not values_dict.get(key, ''):
            raise ValueError('Missing server %s' % key)

    def serialize(self):
        return {
            "id": str(self.id),
            "nombre": self.nombre,
            "token": self.token
        }
