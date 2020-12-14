import json
from base64 import b64decode


def build_user(n=0, role='host'):
    nstr = (str(n) if n > 0 else '')
    return {
        'email': 'test%s@test.com' % nstr,
        'name': 'name%s' % nstr,
        'surname': 'surname%s' % nstr,
        'password': 'test%sPass' % nstr,
        'phone': '0123456789',
        'city': 'test city, test state',
        'role': role
    }


def create_user(client, data_dict):
    res = client.post(path='/v1/usuarios', data=json.dumps(data_dict), content_type='application/json')
    return res.status_code, json.loads(res.data.decode())


def validate_create_user_response(status, res, role):
    assert status == 200
    assert res['id']
    assert res['email'] == 'test@test.com'
    assert res['name'] == 'name'
    assert res['surname'] == 'surname'
    assert res['phone'] == '0123456789'
    assert res['city'] == 'test city, test state'
    assert res['role'] == role


def test_create_user_host_role(client):
    user = build_user(role='host')

    status, res = create_user(client, user)

    validate_create_user_response(status, res, 'host')


def test_create_user_guest_role(client):
    user = build_user(role='guest')

    status, res = create_user(client, user)

    validate_create_user_response(status, res, 'guest')


def test_create_user_admin_role(client):
    user = build_user(role='admin')

    status, res = create_user(client, user)

    validate_create_user_response(status, res, 'admin')


def test_create_user_existing_user(client):
    user = build_user(role='admin')

    status, res = create_user(client, user)
    status, res = create_user(client, user)

    assert status == 400
    assert res['message'] == 'User already exists'


def test_create_user_invalid_role(client):
    user = build_user(role='invalidrole')

    status, res = create_user(client, user)

    assert status == 400
    assert res['message'] == 'Invalid user role'


def test_create_user_missing_name(client):
    status, res = create_user(client, {
        'surname': 'testSurname',
        'email': 'test@test.com',
        'password': 'testPass'
    })

    assert status == 400
    assert res['message'] == 'Missing user name'


def test_create_user_invalid_name(client):
    status, res = create_user(client, {
        'name': '',
        'surname': 'testSurname',
        'email': 'test@test.com',
        'password': 'testPass'
    })

    assert status == 400
    assert res['message'] == 'Missing user name'


def test_create_user_missing_surname(client):
    status, res = create_user(client, {
        'name': 'testName',
        'email': 'test@test.com',
        'password': 'testPass'
    })

    assert status == 400
    assert res['message'] == 'Missing user surname'


def test_create_user_invalid_surname(client):
    status, res = create_user(client, {
        'name': 'testName',
        'surname': '',
        'email': 'test@test.com',
        'password': 'testPass'
    })

    assert status == 400
    assert res['message'] == 'Missing user surname'


def test_create_user_missing_email(client):
    status, res = create_user(client, {
        'name': 'testName',
        'surname': 'testSurname',
        'password': 'testPass'
    })

    assert status == 400
    assert res['message'] == 'Missing user email'


def test_create_user_invalid_name(client):
    status, res = create_user(client, {
        'name': '',
        'surname': 'testSurname',
        'email': 'test@test.com',
        'password': 'testPass'
    })

    assert status == 400
    assert res['message'] == 'Missing user name'


def test_create_user_empty_email(client):
    status, res = create_user(client, {
        'email': '',
        'name': 'testName',
        'surname': 'testSurname',
        'password': 'testPass'
    })

    assert status == 400
    assert res['message'] == 'Missing user email'


def test_create_user_missing_password(client):
    status, res = create_user(client, {
        'name': 'testName',
        'email': 'test@test.com',
        'surname': 'testSurname',
    })

    assert status == 400
    assert res['message'] == 'Missing user password'


def test_create_user_empty_password(client):
    status, res = create_user(client, {
        'name': 'testName',
        'surname': 'testSurname',
        'email': 'test@test.com',
        'password': ''
    })

    assert status == 400
    assert res['message'] == 'Missing user password'


def test_create_user_invalid_password(client):
    status, res = create_user(client, {
        'name': 'testName',
        'surname': 'testSurname',
        'email': 'test@test.com',
        'password': 'short'
    })

    assert status == 400
    assert res['message'] == 'Invalid user password: expected length of 8 characters'


def test_create_user_missing_optional_fields(client):
    status, res = create_user(client, {
        'name': 'testName',
        'surname': 'testSurname',
        'email': 'test@test.com',
        'password': 'password',
        'role': 'guest'
    })

    assert status == 200
    assert res['id']
    assert res['name'] == 'testName'
    assert res['surname'] == 'testSurname'
    assert res['email'] == 'test@test.com'
    assert res['role'] == 'guest'


def test_get_roles(client):
    res = client.get(path='/v1/roles')

    res_json = res.get_json()

    assert res.status_code == 200
    assert res_json['roles'] == ['admin', 'guest', 'host']


def test_create_and_list_users(client):
    create_user(client, build_user(1))
    create_user(client, build_user(2))

    res = client.get(path='/v1/usuarios')

    users_array = json.loads(res.data.decode())

    assert len(users_array) == 2


def test_login(client):
    user = build_user(role='guest')
    create_user(client, user)

    res = client.post(path='/v1/sesiones', data=json.dumps({
        'email': user['email'],
        'password': user['password']
    }), content_type='application/json')

    base64_data = res.get_json()['token'].split('.')[1]

    if len(base64_data) % 2 != 0:
        base64_data += '='

    decoded_data = b64decode(base64_data.encode()).decode()
    data = json.loads(decoded_data)

    assert res.status_code == 200
    assert data['id']
    assert data['email'] == 'test@test.com'
    assert data['role'] == 'guest'
    assert data['exp']


def test_login_wrong_password(client):
    user = build_user()
    create_user(client, user)

    res = client.post(path='/v1/sesiones', data=json.dumps({
        'email': user['email'],
        'password': 'wrongpassword'
    }), content_type='application/json')

    res_json = res.get_json()

    assert res.status_code == 401
    assert res_json['message'] == 'User not recognized'


def test_login_wrong_user(client):
    user = build_user()
    create_user(client, user)

    res = client.post(path='/v1/sesiones', data=json.dumps({
        'email': 'wronguser@test.com',
        'password': user['password']
    }), content_type='application/json')

    res_json = res.get_json()

    assert res.status_code == 401
    assert res_json['message'] == 'User not recognized'


def test_login_empty_header(client):
    user = build_user()
    create_user(client, user)

    res = client.post(path='/v1/sesiones', data=json.dumps({}), content_type='application/json')

    res_json = res.get_json()

    assert res.status_code == 401
    assert res_json['message'] == 'User not recognized'
