from project.db import db
from project.models.user import User, BookBnBUser, OAuthUser


class UserService:

    def _create_user(self, clazz, values):
        user = clazz(**values)

        if self.find_by_email(user.email) is not None:
            raise ValueError('User already exists')

        db.session.add(user)
        db.session.commit()

        return user

    def create_user(self, values_dict):
        return self._create_user(BookBnBUser, values_dict)

    def create_oauth_user(self, values_dict):
        return self._create_user(OAuthUser, values_dict)

    def get_all(self):
        return User.query.all()

    def get(self, user_id):
        return User.query.get(user_id)

    def find_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def get_many(self, ids):
        return User.query.filter(User.id.in_(ids)).all()
