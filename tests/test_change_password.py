import datetime
import json

from project.infra.tokenizer import Tokenizer

from test_create_and_login_users import build_user, create_user


def change_password(client, user, token=''):
    return client.put(
        path='/v1/usuarios/%s/contrasena' % user['email'],
        data=json.dumps({
            'password': 'newpassword'
        }),
        content_type='application/json',
        headers=[('Authorization', token)] if token else []
    )


def test_change_password_success(client, tokenizer):
    user = build_user(role='host')

    status, res = create_user(client, user)

    token = tokenizer.encode({
        'email': user['email'],
        'type': 'change_password',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
    })

    res = change_password(client, user, token)

    assert res.status_code == 200
    assert res.get_json()['message'] == 'ok'


def test_change_password_expired_token(client, tokenizer):
    user = build_user(role='host')

    status, res = create_user(client, user)
    
    token = tokenizer.encode({
        'email': user['email'],
        'type': 'change_password',
        'exp': datetime.datetime.utcnow() - datetime.timedelta(days=1),
    })

    res = change_password(client, user, token)

    assert res.status_code == 400
    assert res.get_json()['message'] == 'Token expired'


def test_change_password_invalid_signature(client):
    user = build_user(role='host')

    status, res = create_user(client, user)
    
    token = Tokenizer('fakekey').encode({
        'email': user['email'],
        'type': 'change_password',
        'exp': datetime.datetime.utcnow() - datetime.timedelta(days=1),
    })

    res = change_password(client, user, token)

    assert res.status_code == 400
    assert res.get_json()['message'] == 'Invalid token signature'


def test_change_password_email_missmatch(client, tokenizer):
    user = build_user(role='host')

    status, res = create_user(client, user)
    
    token = tokenizer.encode({
        'email': 'adifferentemail@example.com',
        'type': 'change_password',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
    })

    res = change_password(client, user, token)

    assert res.status_code == 403
    assert res.get_json()['message'] == 'Token email does not match'


def test_change_password_invalid_role(client, tokenizer):
    user = build_user(role='host')

    status, res = create_user(client, user)
    
    token = tokenizer.encode({
        'email': user['email'],
        'type': 'another_type',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
    })

    res = change_password(client, user, token)

    assert res.status_code == 403
    assert res.get_json()['message'] == 'Invalid token type'


def test_change_password_not_authorized(client):
    user = build_user(role='host')

    status, res = create_user(client, user)

    res = change_password(client, user)

    assert res.status_code == 401
    assert res.get_json()['message'] == 'User not recognized'


