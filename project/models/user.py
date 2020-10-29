from project.db import db

class User(db.Model):
    __tablename__ = "users"

    email = db.Column(db.String(128), unique=True, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(128), nullable=False)

    def __init__(self, email, name, password, role):
        self.email = email
        self.name = name
        self.password = password
        self.role = role

    def serialize(self):
        return {
            "email": self.email,
            "name": self.name,
            "role": self.role
        }
