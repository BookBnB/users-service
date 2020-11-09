from project.db import db
from project.models.user import User
from werkzeug.security import generate_password_hash
from project.models.role import ROLES

class UserService():
    def assert_key(self, values_dict, key):
        if not values_dict.get(key, ''):
            raise ValueError('Missing user %s' % key)

    def create_user(self, values_dict):
        self.assert_key(values_dict, 'name')
        self.assert_key(values_dict, 'surname')
        self.assert_key(values_dict, 'email')
        self.assert_key(values_dict, 'password')

        if len(values_dict['password']) < 8:
            raise ValueError('Invalid user password: expected length of 8 characters')

        if values_dict.get('role', '') not in ROLES:
            raise ValueError('Invalid user role')

        if self.find_by_email(values_dict['email']) is not None:
            raise ValueError('User already exists')

        hashed_password = generate_password_hash(values_dict['password'], method='sha256')

        user = User(values_dict['email'], values_dict['name'], values_dict['surname'],
                    hashed_password, values_dict['role'], values_dict['phone'],
                    values_dict['city'])

        db.session.add(user)
        db.session.commit()

        return user

    def get_all(self):
        return User.query.all()

    def find_by_email(self, email):
        return User.query.filter_by(email=email).first()
