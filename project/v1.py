import datetime

import jwt
from flasgger import swag_from
from flask import (Blueprint, current_app, jsonify, make_response,
                   request)

from project.infra.google_oauth import OAuth, TokenError
from project.models.role import ROLES
from project.services.users_service import UserService

bp = Blueprint('v1', __name__, url_prefix='/v1')

@bp.route('/usuarios', methods=['POST'])
@swag_from('swagger/users/post/users.yml')
def users_create():
    body = request.get_json()

    try:
        service = UserService()
        user = service.create_user(body)

        return jsonify(user.serialize())
    except ValueError as ex:
        return make_response({ 'message': str(ex) }, 400)

@bp.route('/usuarios/google', methods=['POST'])
@swag_from('swagger/users/post/google-users.yml')
def google_users_create():
    oauth = OAuth(current_app.config['GOOGLE_CLIENT_ID'])
    body = request.get_json()
    users_service = UserService()

    try:
        info = oauth.verify(body['token'])
        user = users_service.create_oauth_user({
            'name': info['given_name'],
            'surname': info['family_name'],
            'email': info['email'],
            'role': body.get('role', None),
            'phone': body.get('phone', None),
            'city': body.get('city', None)
        })
        return jsonify(user.serialize())
    except TokenError as e:
        return make_response({'error': 'TokenError', 'message': str(e)}, 400)

@bp.route('/usuarios', methods=['GET'])
@swag_from('swagger/users/get/users.yml')
def users_list():
    users = UserService().get_all()
    return jsonify([u.serialize() for u in users])

@bp.route('/sesiones', methods=['POST'])
@swag_from('swagger/users/post/sessions.yml')
def create_session():
    data = request.get_json()

    email = data.get('email', '')
    password = data.get('password', '')

    if not email or not password:
        return make_response({ 'message': 'User not recognized' }, 401)

    user = UserService().find_by_email(email)

    if not user:
        return make_response({ 'message': 'User not recognized' }, 401)

    if user.password_matches(password):
        token_duration = datetime.timedelta(seconds=current_app.config['SESSION_TOKEN_DURATION'])

        token = jwt.encode({
                'id': str(user.id),
                'email': user.email,
                'exp': datetime.datetime.utcnow() + token_duration,
                'role': user.role
            },
            current_app.config['SECRET_KEY']
        )
        return jsonify({'token': token.decode('UTF-8')})

    return make_response({ 'message': 'User not recognized' }, 401)

@bp.route('/roles')
@swag_from('swagger/users/get/roles.yml')
def get_roles():
    return jsonify({ 'roles': ROLES })
