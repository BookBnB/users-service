from project.db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    surname = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(128))
    city = db.Column(db.String(128))
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'users'
    }

    def __init__(self, email, name, surname, password, role, phone, city):
        self.email = email
        self.name = name
        self.surname = surname
        self.password = password
        self.role = role
        self.phone = phone
        self.city = city

    def serialize(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "name": self.name,
            "surname": self.surname,
            "role": self.role,
            "phone": self.phone,
            "city": self.city
        }


class BookBnBUser(User):
    password = db.Column(db.String(128), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'bookbnb_user'
    }


class OAuthUser(User):
    __mapper_args__ = {
        'polymorphic_identity': 'oauth_ser'
    }
