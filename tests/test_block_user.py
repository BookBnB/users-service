import json

from freezegun import freeze_time

from tests.test_create_and_login_google_users import VALID_DATE
from tests.test_create_and_login_google_users import \
    VALID_TOKEN as VALID_GOOGLE_TOKEN
from tests.test_create_and_login_google_users import \
    create_user as create_google_user
from tests.test_create_and_login_google_users import login as google_login
from tests.test_create_and_login_users import (build_user, create_user, login,
                                               validate_login_response)
from tests.test_get_users import get_user
import uuid


def create_user_and_login(client, role='host'):
    admin = build_user(role=role, n=9)
    create_user(client, admin)
    status, res = login(client, admin)
    return res['token']

def block_request(client, userId, body, session_token=''):
    res = client.put(
        path='/v1/usuarios/' + userId + '/bloqueo',
        data=json.dumps(body),
        content_type='application/json',
        headers=[('Authorization', session_token)] if session_token else []
    )
    return res.status_code, json.loads(res.data.decode())

def block_user(client, userId, session_token=''):
    return block_request(client, userId, {'blocked': True}, session_token)

def unblock_user(client, userId, session_token=''):
    return block_request(client, userId, {'blocked': False}, session_token)

def test_block_user(client):
    token = create_user_and_login(client, role='admin')

    user = build_user(role='guest')
    status, res = create_user(client, user)
    user_id = res['id']

    status, res = block_user(client, user_id, session_token=token)

    status, res = get_user(client, user_id)

    assert status == 200
    assert res['blocked'] == True

def test_block_user_login(client):
    token = create_user_and_login(client, role='admin')

    user = build_user(role='guest')
    status, res = create_user(client, user)
    user_id = res['id']

    status, res = block_user(client, user_id, session_token=token)

    status, res = login(client, user)

    assert status == 403
    assert res['message'] == 'User is blocked'

@freeze_time(VALID_DATE)
def test_block_user_google_login(client):
    token = create_user_and_login(client, role='admin')

    user = build_user(role='guest')
    status, res = create_google_user(client, VALID_GOOGLE_TOKEN)
    user_id = res['id']

    status, res = block_user(client, user_id, session_token=token)

    status, res = google_login(client, VALID_GOOGLE_TOKEN)

    assert status == 403
    assert res['message'] == 'User is blocked'

def test_block_unblock_user(client):
    token = create_user_and_login(client, role='admin')

    user = build_user(role='guest')
    status, res = create_user(client, user)
    user_id = res['id']

    status, res = block_user(client, user_id, session_token=token)
    status, res = unblock_user(client, user_id, session_token=token)

    status, res = get_user(client, user_id)

    assert status == 200
    assert res['blocked'] == False


def test_block_user_invalid_id(client):
    token = create_user_and_login(client, role='admin')

    user = build_user(role='guest')
    status, res = create_user(client, user)

    status, res = block_user(client, 'aninvalidid')

    assert status == 400
    assert res['message'] == 'Invalid id aninvalidid'


def test_block_user_non_admin(client):
    token = create_user_and_login(client, role='host')

    user = build_user(role='guest')
    status, res = create_user(client, user)
    user_id = str(uuid.uuid4())

    status, res = block_user(client, user_id, session_token=token)

    assert status == 403
    assert res['message'] == 'Only an admin can block users'


def test_block_user_not_authenticated(client):
    user = build_user(role='guest')
    status, res = create_user(client, user)
    user_id = str(uuid.uuid4())

    status, res = block_user(client, user_id)

    assert status == 401
    assert res['message'] == 'User not recognized'
