import datetime

import jwt
from flask import Blueprint, Flask, jsonify, make_response, request, current_app
from werkzeug.security import check_password_hash, generate_password_hash

from project.db import db
from project.models.user import User

bp = Blueprint('v1', __name__, url_prefix='/v1')

@bp.route('/users', methods=['POST'])
def users_create():
	body = request.get_json()

	hashed_password = generate_password_hash(body['password'], method='sha256')

	u = User(body['email'], body['name'], hashed_password)

	db.session.add(u)
	db.session.commit()

	return jsonify(u.serialize())

@bp.route('/users', methods=['GET'])
def users_list():
	users = User.query.all()
	return jsonify([u.serialize() for u in users])

@bp.route('/login')
def login():
	auth = request.authorization

	if not auth or not auth.username or not auth.password:
		return make_response('User not recognized', 401)

	user = User.query.filter_by(email=auth.username).first()

	if not user:
		return make_response('User not recognized', 401)

	if check_password_hash(user.password, auth.password):
		token = jwt.encode({
				'id': user.email,
				'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
			},
			current_app.config['SECRET_KEY']
		)
		return jsonify({'token': token.decode('UTF-8')})

	return make_response('User not recognized', 401)
