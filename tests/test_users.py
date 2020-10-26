import json
from base64 import b64encode, b64decode

def build_user(n=0):
	nstr = (str(n) if n > 0 else '')
	return {
		'name': 'test%sUser' % nstr,
		'password': 'test%sPass' % nstr,
		'email': 'test%s@test.com' % nstr
	}

def create_user(client, data_dict):
	res = client.post(path='/v1/users', data=json.dumps(data_dict), content_type='application/json')
	return res.status_code, json.loads(res.data.decode())

def test_create_user(client):
	user = build_user()

	status, res = create_user(client, user)

	assert status == 200
	assert res['email'] == 'test@test.com'
	assert res['name'] == 'testUser'

def test_create_user_missing_name(client):
	status, res = create_user(client, { 'email': 'test@test.com', 'password': 'testPass' })

	assert status == 400
	assert res['error'] == 'Missing user name'

def test_create_user_invalid_name(client):
	status, res = create_user(client, { 'name': '', 'email': 'test@test.com', 'password': 'testPass' })

	assert status == 400
	assert res['error'] == 'Missing user name'

def test_create_user_missing_email(client):
	status, res = create_user(client, { 'name': 'testName', 'password': 'testPass' })

	assert status == 400
	assert res['error'] == 'Missing user email'

def test_create_user_invalid_name(client):
	status, res = create_user(client, { 'name': '', 'email': 'test@test.com', 'password': 'testPass' })

	assert status == 400
	assert res['error'] == 'Missing user name'

def test_create_user_empty_email(client):
	status, res = create_user(client, { 'email': '', 'name': 'testName', 'password': 'testPass' })

	assert status == 400
	assert res['error'] == 'Missing user email'

def test_create_user_missing_password(client):
	status, res = create_user(client, { 'name': 'testName', 'email': 'test@test.com' })

	assert status == 400
	assert res['error'] == 'Missing user password'

def test_create_user_empty_password(client):
	status, res = create_user(client, { 'name': 'testName', 'email': 'test@test.com', 'password': '' })

	assert status == 400
	assert res['error'] == 'Missing user password'

def test_create_user_invalid_password(client):
	status, res = create_user(client, { 'name': 'testName', 'email': 'test@test.com', 'password': 'short' })

	assert status == 400
	assert res['error'] == 'Invalid user password: expected length of 8 characters'

def test_create_and_list_users(client):
	create_user(client, build_user(1))
	create_user(client, build_user(2))

	res = client.get(path='/v1/users')

	users_array = json.loads(res.data.decode())

	assert len(users_array) == 2

def test_login(client):
	user = build_user()
	create_user(client, user)

	credentials = '{}:{}'.format(user['email'], user['password'])
	encoded_credentials = b64encode(credentials.encode()).decode()

	auth_header = ('Authorization', 'Basic {}'.format(encoded_credentials))

	res = client.get(path='/v1/login', headers=[auth_header])

	base64_data = res.get_json()['token'].split('.')[1]
	decoded_data = b64decode(base64_data.encode()).decode()
	data = json.loads(decoded_data)

	assert data['id'] == 'test@test.com'
	assert res.status_code == 200

def test_login_wrong_password(client):
	user = build_user()
	create_user(client, user)

	credentials = '{}:{}'.format(user['email'], 'wrongPassword')
	encoded_credentials = b64encode(credentials.encode()).decode()

	auth_header = ('Authorization', 'Basic {}'.format(encoded_credentials))

	res = client.get(path='/v1/login', headers=[auth_header])
	res_json = res.get_json()

	assert res.status_code == 401
	assert res_json['error'] == 'User not recognized'

def test_login_wrong_user(client):
	user = build_user()
	create_user(client, user)

	credentials = '{}:{}'.format('anotheruser@test.com', user['password'])
	encoded_credentials = b64encode(credentials.encode()).decode()

	auth_header = ('Authorization', 'Basic {}'.format(encoded_credentials))

	res = client.get(path='/v1/login', headers=[auth_header])
	res_json = res.get_json()

	assert res.status_code == 401
	assert res_json['error'] == 'User not recognized'

def test_login_missing_header(client):
	user = build_user()
	create_user(client, user)

	res = client.get(path='/v1/login')
	res_json = res.get_json()

	assert res.status_code == 401
	assert res_json['error'] == 'User not recognized'
