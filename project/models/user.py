from project.db import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    new_field = db.Column(db.Integer, default=0, nullable=False)
    other_new_field = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "new_field": self.new_field
        }
