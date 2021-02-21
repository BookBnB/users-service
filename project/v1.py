import datetime

from flasgger import swag_from
from sqlalchemy import exc
import psycopg2
from flask import (Blueprint, current_app, jsonify, make_response,
                   request)

from project.infra.google_oauth import OAuth, TokenError
from project.infra.tokenizer import Tokenizer
from project.models.role import ROLES
from project.models.user import UserDoesntHavePasswordError
from project.services.users_service import UserService
from project.services.servers_service import ServerService

bp = Blueprint('v1', __name__, url_prefix='/v1')


@bp.route('/usuarios', methods=['POST'])
@swag_from('swagger/users/post/users.yml')
def users_create(users: UserService):
    body = request.get_json()

    try:
        user = users.create_user(body)
        return jsonify(user.serialize()), 201
    except ValueError as ex:
        return make_response({'message': str(ex)}, 400)


@bp.route('/usuarios/google', methods=['POST'])
@swag_from('swagger/users/post/google-users.yml')
def google_users_create(users: UserService, oauth: OAuth):
    body = request.get_json()

    token = body.get('token', None)

    if not token:
        return make_response({'message': 'Missing token'}, 400)

    try:
        info = oauth.verify(token)
        user = users.create_oauth_user({
            'name': info['given_name'],
            'surname': info['family_name'],
            'email': info['email'],
            'role': body.get('role', None),
            'phone': body.get('phone', None),
            'city': body.get('city', None)
        })
        return jsonify(user.serialize()), 201
    except TokenError as e:
        return make_response({'error': 'TokenError', 'message': str(e)}, 400)


@bp.route('/usuarios/<id>', methods=['GET'])
@swag_from('swagger/users/get/user.yml')
def user_find(id, users: UserService):
    try:
        user = users.get(id)
    except exc.DataError:
        return make_response({'message': 'Invalid id {}'.format(id)}, 400)

    if not user:
        return make_response({'message': 'User with id {} does not exist'.format(id)}, 404)
    return jsonify(user.serialize())


@bp.route('/usuarios/bulk', methods=['GET'])
@swag_from('swagger/users/get/bulk_users.yml')
def users_find(users: UserService):
    ids = request.args.getlist('id')
    try:
        users = users.get_many(ids)
    except exc.DataError:
        return make_response({'message': 'Invalid parameters'}, 400)

    if len(users) != len(ids):
        return make_response({'message': 'One or more users do not exist'.format(id)}, 404)

    return jsonify([user.serialize() for user in users])


@bp.route('/usuarios', methods=['GET'])
@swag_from('swagger/users/get/users.yml')
def users_list(users: UserService):
    users = users.get_all()
    return jsonify([u.serialize() for u in users])


@bp.route('/sesiones', methods=['POST'])
@swag_from('swagger/users/post/sessions.yml')
def create_session(users: UserService, tokenizer: Tokenizer):
    data = request.get_json()

    email = data.get('email', None)
    password = data.get('password', None)

    if not email or not password:
        return make_response({'message': 'User or password missing'}, 400)

    user = users.find_by_email(email)

    try:
        if not user or not user.password_matches(password):
            return make_response({'message': 'User not recognized'}, 401)
    except UserDoesntHavePasswordError:
        return make_response({'message': 'User doesn\'t have password'}, 401)

    return jsonify({'token': _generate_session_token(tokenizer, user)})


@bp.route('/sesiones/google', methods=['POST'])
@swag_from('swagger/users/post/google-sessions.yml')
def create_google_session(users: UserService, tokenizer: Tokenizer, oauth: OAuth):
    body = request.get_json()

    token = body.get('token', None)

    if not token:
        return make_response({'message': 'Missing token'}, 400)

    try:
        info = oauth.verify(token)
    except TokenError as e:
        return make_response({'error': 'TokenError', 'message': str(e)}, 400)

    user = users.find_by_email(info['email'])

    if not user:
        return make_response({'message': 'User not recognized'}, 401)

    return jsonify({'token': _generate_session_token(tokenizer, user)})


def _generate_session_token(tokenizer, user):
    token_duration = datetime.timedelta(seconds=current_app.config['SESSION_TOKEN_DURATION'])
    return tokenizer.encode({
        'id': str(user.id),
        'email': user.email,
        'exp': datetime.datetime.utcnow() + token_duration,
        'role': user.role
    }).decode('UTF-8')


@bp.route('/roles')
@swag_from('swagger/users/get/roles.yml')
def get_roles():
    return jsonify({'roles': ROLES})


@bp.route('/servidores', methods=['POST'])
@swag_from('swagger/servers/post/servers.yml')
def servers_create(servers: ServerService):
    body = request.get_json()

    try:
        server = servers.create_server(body)
        return jsonify(server.serialize()), 201
    except ValueError as ex:
        return make_response({'message': str(ex)}, 400)


@bp.route('/servidores', methods=['GET'])
@swag_from('swagger/servers/get/servers.yml')
def servers_list(servers: ServerService):
    servers = servers.get_all()
    return jsonify([u.serialize() for u in servers])
