from flask import Flask, jsonify, Blueprint, request, make_response
from project.db import db
from project.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

bp = Blueprint('v1', __name__, url_prefix='/v1')

@bp.route("/")
def hello_world():
	return jsonify(hello="world")

@bp.route("/test")
def test_endpoint():
	return jsonify(result="ok!")

#TODO: esto no deberia venir por path variable
@bp.route("/users/<email>/<name>/<password>", methods=["POST"])
def user_create(email, name, password):
	hashed_password = generate_password_hash(password, method='sha256')
	u = User(email, name, hashed_password)
	db.session.add(u)
	db.session.commit()
	return jsonify(u.serialize())

@bp.route("/users")
def users():
	users = User.query.all()
	return jsonify([u.serialize() for u in users])

@bp.route("/login")
def login():
	auth = request.authorization

	if not auth or not auth.username or not auth.password:
		return make_response('User not recognized', 401)

	user = User.query.filter_by(name=auth.username).first()

	if not user:
		return make_response('User not recognized', 401)

	if check_password_hash(user.password, auth.password):
		token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, bp.config['SECRET_KEY'])
		return jsonify({'token': token.decode('UTF-8')})

	return make_response('User not recognized', 401)