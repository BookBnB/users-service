import json
from tests.test_create_and_login_users import create_user, build_user


def validate_same_user(user, res):
    assert res['id']
    assert res['email'] == user['email']
    assert res['name'] == user['name']
    assert res['surname'] == user['surname']
    assert res['phone'] == user['phone']
    assert res['city'] == user['city']
    assert res['role'] == user['role']


def get_user(client, id):
    res = client.get(path='/v1/usuarios/' + id)
    return res.status_code, json.loads(res.data.decode())


def get_several_users(client, ids):
    query = '&id='.join(ids)
    res = client.get(path='/v1/usuarios/bulk?id=' + query)
    return res.status_code, json.loads(res.data.decode())


def test_get_user(client):
    user = build_user(role='host')
    status, res = create_user(client, user)

    status, res = get_user(client, res['id'])
    assert status == 200
    validate_same_user(user, res)


def test_get_nonexistent_user(client):
    status, res = get_user(client, 'bde73625-76d6-4590-bb39-ead4db61ceb6')
    assert status == 404


def test_get_user_invalid_id(client):
    status, res = get_user(client, 'invalid_id')
    assert status == 400


def test_get_many_users(client):
    ids = []
    users = []
    for i in range(10):
        user = build_user(n=i, role='host')
        users.append(user)
        status, res = create_user(client, user)
        ids.append(res['id'])

    status, res = get_several_users(client, ids)

    assert status == 200
    for i in range(10):
        validate_same_user(users[i], res[i])


def test_get_many_users_with_nonexistent_user(client):
    status, res = get_several_users(client, ['bde73625-76d6-4590-bb39-ead4db61ceb6'])
    assert status == 404


def test_get_users_with_invalid_id(client):
    status, res = get_several_users(client, ['invalid_id'])
    assert status == 400
