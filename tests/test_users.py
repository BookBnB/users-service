import json

def build_user(n=0):
	nstr = (str(n) if n > 0 else '')
	return {
		'name': 'test%sUser' % nstr,
		'password': 'test%sPass' % nstr,
		'email': 'test%s@test.com' % nstr
	}

def test_create_user(client):
	user = build_user()

	res = client.post(path='/v1/users', data=json.dumps(user), content_type='application/json')
	res_json = json.loads(res.data.decode())

	assert res.status_code == 200
	assert res_json['email'] == 'test@test.com'
	assert res_json['name'] == 'testUser'

def test_create_and_list_users(client):
	res = client.post(path='/v1/users', data=json.dumps(build_user(1)), content_type='application/json')
	res = client.post(path='/v1/users', data=json.dumps(build_user(2)), content_type='application/json')

	res = client.get(path='/v1/users')

	users_array = json.loads(res.data.decode())

	assert len(users_array) == 2

