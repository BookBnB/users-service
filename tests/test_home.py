import json

def test_home(client):
    res = client.get('/v1/')
    assert res.data == b'{"hello":"world"}\n'

def test_create_user(client):
    res = client.post(path='/v1/users/test@test.com/testUser/testPass')
    assert res.data == b'{"message":"ok"}\n'

def test_create_and_list_users(client):
    res = client.post(path='/v1/users/test1@test.com/testUser1/testPass1')
    res = client.post(path='/v1/users/test2@test.com/testUser2/testPass2')

    res = client.get(path='/v1/users')
    print(res)
    users_array = json.loads(res.data.decode())
    assert len(users_array) == 2

