import datetime

import jwt
from flask import (Blueprint, Flask, current_app, jsonify, make_response,
                   request)
from werkzeug.security import check_password_hash, generate_password_hash

from project.db import db
from project.services.users_service import UserService
from project.models.role import ROLES

bp = Blueprint('v1', __name__, url_prefix='/v1')

@bp.route('/users', methods=['POST'])
def users_create():
	body = request.get_json()

	try:
		service = UserService()
		user = service.create_user(body)

		return jsonify(user.serialize())
	except ValueError as ex:
		return make_response({ 'error': str(ex) }, 400)

@bp.route('/users', methods=['GET'])
def users_list():
	users = UserService().get_all()
	return jsonify([u.serialize() for u in users])

@bp.route('/session', methods=['POST'])
def create_session():
    data = request.get_json()

    email = data.get('email', '')
    password = data.get('password', '')

    if not email or not password:
        return make_response({ 'error': 'User not recognized' }, 401)

    user = UserService().find_by_email(email)

    if not user:
        return make_response({ 'error': 'User not recognized' }, 401)

    if check_password_hash(user.password, password):
        token = jwt.encode({
                'id': user.email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                'role': user.role
            },
            current_app.config['SECRET_KEY']
        )
        return jsonify({'token': token.decode('UTF-8')})

    return make_response({ 'error': 'User not recognized' }, 401)

@bp.route('/roles')
def get_roles():
    return jsonify({ 'roles': ROLES })
