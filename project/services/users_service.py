from project.db import db
from project.models.user import User
from werkzeug.security import generate_password_hash
from project.models.role import ROLES

class UserService():
    def create_user(self, values_dict):
        if not values_dict.get('name', ''):
            raise ValueError('Missing user name')

        if not values_dict.get('email', ''):
            raise ValueError('Missing user email')

        if not values_dict.get('password', ''):
            raise ValueError('Missing user password')

        if len(values_dict['password']) < 8:
            raise ValueError('Invalid user password: expected length of 8 characters')

        if values_dict.get('role', '') not in ROLES:
            raise ValueError('Invalid user role')

        hashed_password = generate_password_hash(values_dict['password'], method='sha256')

        user = User(values_dict['email'], values_dict['name'], hashed_password, values_dict['role'])

        db.session.add(user)
        db.session.commit()

        return user

    def get_all(self):
        return User.query.all()

    def find_by_email(self, email):
        return User.query.filter_by(email=email).first()
