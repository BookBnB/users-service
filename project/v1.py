import datetime
import traceback
from functools import wraps
from time import strftime

import psycopg2
from flasgger import swag_from
from flask import Blueprint, current_app, jsonify, make_response, request
from sqlalchemy import exc

from project.infra.google_oauth import OAuth, TokenError
from project.infra.mail_service import MailService
from project.infra.tokenizer import (ExpiredSignatureError,
                                     InvalidSignatureError, Tokenizer)
from project.models.role import ROLES
from project.models.user import UserDoesntHavePasswordError
from project.services.servers_service import ServerService
from project.services.users_service import UserService

bp = Blueprint('v1', __name__, url_prefix='/v1')


def api_key_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if not current_app.config['REQUIRE_API_KEY']:
            return func(*args, **kwargs)

        token = request.headers.get('x-api-key')

        if not token:
            return make_response({ 'message': 'Missing API key'}, 403)

        server = ServerService().find_by_token(token)

        if not server:
            return make_response({ 'message': 'Invalid API key'}, 403)

        if server.blocked:
            return make_response({ 'message': 'Blocked API key' }, 403)

        return func(*args, **kwargs)

    return decorated


@bp.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    current_app.logger.info('%s %s %s %s', request.method, request.scheme, request.full_path, response.status)
    return response


@bp.errorhandler(Exception)
def exceptions(e):
    tb = traceback.format_exc()
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    current_app.logger.error('%s %s %s 5xx INTERNAL SERVER ERROR\n%s', request.method, request.scheme, request.full_path, tb)
    
    if hasattr(e, 'status_code'):
        return e.status_code
    return 500


@swag_from('swagger/users/post/users.yml')
@bp.route('/usuarios', methods=['POST'])
@api_key_required
def users_create(users: UserService):
    body = request.get_json()

    try:
        user = users.create_user(body)
        return jsonify(user.serialize()), 201
    except ValueError as ex:
        return make_response({'message': str(ex)}, 400)


@bp.route('/usuarios/google', methods=['POST'])
@swag_from('swagger/users/post/google-users.yml')
@api_key_required
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
@api_key_required
def user_find(id, users: UserService):
    try:
        user = users.get(id)
    except exc.DataError:
        return make_response({'message': 'Invalid id {}'.format(id)}, 400)

    if not user:
        return make_response({'message': 'User with id {} does not exist'.format(id)}, 404)
    return jsonify(user.serialize())


@bp.route('/usuarios/<id>', methods=['PUT'])
@swag_from('swagger/users/put/users.yml')
def user_update(id, users: UserService):
    try:
        user = users.get(id)
    except exc.DataError:
        return make_response({'message': 'Invalid id {}'.format(id)}, 400)

    if not user:
        return make_response({'message': 'User with id {} does not exist'.format(id)}, 404)

    values = request.get_json()
    user.update(values)
    users.save(user)

    return make_response({ 'message': 'ok' }, 200)


@bp.route('/usuarios/<id>/bloqueo', methods=['PUT'])
@swag_from('swagger/users/put/users-block.yml')
@api_key_required
def block_user(id, users: UserService, tokenizer: Tokenizer):
    try:
        user = users.get(id)
    except exc.DataError:
        return make_response({'message': 'Invalid id {}'.format(id)}, 400)

    if not request_is_authenticated():
        return make_response({'message': 'User not recognized'}, 401)

    if not request_is_from_role('admin', tokenizer):
        return make_response({'message': 'Only an admin can block users'}, 403)

    if not user:
        return make_response({'message': 'User with id {} does not exist'.format(id)}, 404)

    body = request.get_json()

    user.blocked = bool(body['blocked'])

    users.save(user)

    return jsonify({})

@bp.route('/usuarios/bulk', methods=['GET'])
@swag_from('swagger/users/get/bulk_users.yml')
@api_key_required
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
@api_key_required
def users_list(users: UserService):
    users = users.get_all()
    return jsonify([u.serialize() for u in users])


@bp.route('/sesiones', methods=['POST'])
@swag_from('swagger/users/post/sessions.yml')
@api_key_required
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
        if user.blocked:
            return make_response({'message': 'User is blocked'}, 403)
    except UserDoesntHavePasswordError:
        return make_response({'message': 'User doesn\'t have password'}, 401)

    return jsonify({'token': _generate_session_token(tokenizer, user)})


@bp.route('/sesiones/google', methods=['POST'])
@swag_from('swagger/users/post/google-sessions.yml')
@api_key_required
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

    if user.blocked:
        return make_response({'message': 'User is blocked'}, 403)

    return jsonify({'token': _generate_session_token(tokenizer, user)})


def _generate_session_token(tokenizer, user):
    token_duration = datetime.timedelta(seconds=current_app.config['SESSION_TOKEN_DURATION'])
    return tokenizer.encode({
        'id': str(user.id),
        'email': user.email,
        'exp': datetime.datetime.utcnow() + token_duration,
        'role': user.role
    }).decode('UTF-8')


def request_is_authenticated():
    return request.headers.get('Authorization') != None


def request_is_from_role(role, tokenizer):
    auth_header = request.headers.get('Authorization')
    decoded_token = tokenizer.decode(auth_header.encode(), verify_signature=False)
    return decoded_token['role'] == role


@bp.route('/roles')
@swag_from('swagger/users/get/roles.yml')
@api_key_required
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


@bp.route('/servidores/<name>/bloqueo', methods=['PUT'])
# @swag_from('swagger/servers/get/servers.yml')
def block_server(name, servers: ServerService):
    server = servers.find_by_name(name)

    if not server:
        return make_response({'message': 'Server does not exist'}, 404)

    body = request.get_json()

    server.blocked = bool(body['bloqueado'])

    servers.save(server)

    return make_response({ 'message': 'ok' }, 200)


@bp.route('/usuarios/<email>/recuperacion', methods=['PUT'])
@swag_from('swagger/users/put/recover.yml')
@api_key_required
def cambiarContrasena(email, users: UserService, tokenizer: Tokenizer, mailService: MailService):
    user = users.find_by_email(email)

    if not user:
        return make_response({'message': 'User does not exist'}, 404)

    duration = datetime.timedelta(seconds=current_app.config['CHANGE_PASSWORD_TOKEN_DURATION'])
    token = tokenizer.encode({
        'id': str(user.id),
        'email': user.email,
        'exp': datetime.datetime.utcnow() + duration,
        'type': 'change_password'
    }).decode('UTF-8')

    content = 'Ingrese al siguiente enlace para cambiar su contraseña: %s/change-password?jwt=%s' % (
        current_app.config['BACKOFFICE_URL'],
        token
    )

    mailService.send_mail(
        'Cambio de contraseña',
        user.email,
        current_app.config['MAIL_DEFAULT_SENDER'],
        content
    )

    return make_response({'message': 'ok'}, 200)


@bp.route('/usuarios/<email>/contrasena', methods=['PUT'])
@swag_from('swagger/users/put/password.yml')
@api_key_required
def confirmarCambioContrasena(email, users: UserService, tokenizer: Tokenizer):
    try:
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return make_response({'message': 'User not recognized'}, 401)

        decoded_token = tokenizer.decode(auth_header.encode())

        if decoded_token['type'] != 'change_password':
            return make_response({'message': 'Invalid token type'}, 403)

        if decoded_token['email'] != email:
            return make_response({'message': 'Token email does not match'}, 403)

        body = request.get_json()

        user = users.find_by_email(email)

        user.change_password(body['password'])

        users.save(user)

        return make_response({'message': 'ok'}, 200)
    except ExpiredSignatureError as e:
        return make_response({'message': 'Token expired'}, 400)
    except InvalidSignatureError as e:
        return make_response({'message': 'Invalid token signature'}, 400)
