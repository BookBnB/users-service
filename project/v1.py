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
    """Creación de Usuario
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
            $ref: '#/definitions/CrearUsuarioDTO'
        required: true
    definitions:
      CrearUsuarioDTO:
        type: object
        properties:
          email:
            type: string
          name:
            type: string
          surname:
            type: string
          password:
            type: string
          role:
            type: string
          phone:
            type: string
          city:
            type: string
      UsuarioDTO:
        type: object
        properties:
          id:
            type: string
          email:
            type: string
          name:
            type: string
          surname:
            type: string
          password:
            type: string
          role:
            type: string
          phone:
            type: string
          city:
            type: string
    responses:
      200:
        description: Datos del usuario creado
        schema:
          $ref: '#/definitions/UsuarioDTO'
    """
    body = request.get_json()

    try:
        service = UserService()
        user = service.create_user(body)

        return jsonify(user.serialize())
    except ValueError as ex:
        return make_response({ 'message': str(ex) }, 400)

@bp.route('/users', methods=['GET'])
def users_list():
    """Listado de usuarios
    ---
    responses:
      200:
        description: Listado de usuarios
        schema:
          $ref: '#/definitions/UsuarioDTO'
    """
    users = UserService().get_all()
    return jsonify([u.serialize() for u in users])

@bp.route('/sessions', methods=['POST'])
def create_session():
    """Crear una sesión para un usuario
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
            $ref: '#/definitions/CrearSesionDTO'
        required: true
    definitions:
        CrearSesionDTO:
            type: object
            properties:
                email:
                    type: string
                password:
                    type: string
        SesionDTO:
            type: object
            properties:
                token:
                    type: string
    responses:
        200:
            description: Objeto con token de sesión creada
            schema:
                $ref: '#/definitions/SesionDTO'
    """
    data = request.get_json()

    email = data.get('email', '')
    password = data.get('password', '')

    if not email or not password:
        return make_response({ 'message': 'User not recognized' }, 401)

    user = UserService().find_by_email(email)

    if not user:
        return make_response({ 'message': 'User not recognized' }, 401)

    if check_password_hash(user.password, password):
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
def get_roles():
    """Listado de roles
    ---
    definitions:
        UsuarioDTO:
            type: object
            properties:
                roles:
                    type: array
                    items: string
    responses:
        200:
            description: Listado de roles
            schema:
                $ref: '#/definitions/UsuarioDTO'
    """
    return jsonify({ 'roles': ROLES })
