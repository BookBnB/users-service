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
