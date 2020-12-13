from project.db import db
from project.models.user import User, BookBnBUser


class UserService():

    def create_user(self, values_dict):
        user = BookBnBUser(**values_dict)

        if self.find_by_email(user.email) is not None:
            raise ValueError('User already exists')

        db.session.add(user)
        db.session.commit()

        return user

    def create_oauth_user(self, values_dict):
        pass

    def get_all(self):
        return User.query.all()

    def find_by_email(self, email):
        return User.query.filter_by(email=email).first()
