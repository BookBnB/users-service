from project.db import db
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import re

from project.models.role import ROLES


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    surname = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(128))
    city = db.Column(db.String(128))
    type = db.Column(db.String(50), nullable=False)
    blocked = db.Column(db.Boolean(), default=False, nullable=False)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'users'
    }

    def __init__(self, **kwargs):
        self.assert_key(kwargs, 'name')
        self.assert_key(kwargs, 'surname')
        self.assert_key(kwargs, 'email')

        if kwargs.get('role', '') not in ROLES:
            raise ValueError('Invalid user role')

        if not re.match(re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"), kwargs['email']):
            raise ValueError('Invalid email')

        self.email = kwargs['email']
        self.name = kwargs['name']
        self.surname = kwargs['surname']
        self.role = kwargs['role']
        self.phone = kwargs.get('phone', None)
        self.city = kwargs.get('city', None)

    def assert_key(self, values_dict, key):
        if not values_dict.get(key, ''):
            raise ValueError('Missing user %s' % key)

    def serialize(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "name": self.name,
            "surname": self.surname,
            "role": self.role,
            "phone": self.phone,
            "city": self.city,
            "blocked": self.blocked
        }

    def password_matches(self, password):
        raise NotImplementedError()


class BookBnBUser(User):
    password = db.Column(db.String(128))

    __mapper_args__ = {
        'polymorphic_identity': 'bookbnb_user'
    }

    def __init__(self, **kwargs):
        self.assert_key(kwargs, 'password')

        if len(kwargs['password']) < 8:
            raise ValueError('Invalid user password: expected length of 8 characters')

        super().__init__(**kwargs)

        self.change_password(kwargs['password'])

    def password_matches(self, password):
        return check_password_hash(self.password, password)

    def change_password(self, new_password):
        hashed_password = generate_password_hash(new_password, method='sha256')
        self.password = hashed_password



class OAuthUser(User):
    __mapper_args__ = {
        'polymorphic_identity': 'oauth_ser'
    }

    def password_matches(self, password):
        raise UserDoesntHavePasswordError('OAuthUser doesn\'t have password')


class UserDoesntHavePasswordError(Exception):
    pass
