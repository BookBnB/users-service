from project.db import db

class User(db.Model):
    __tablename__ = "users"

    email = db.Column(db.String(128), unique=True, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    surname = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(128))
    city = db.Column(db.String(128))


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
            "email": self.email,
            "name": self.name,
            "surname": self.surname,
            "role": self.role,
            "phone": self.phone,
            "city": self.city
        }
