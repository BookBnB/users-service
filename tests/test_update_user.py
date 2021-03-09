import json

from test_create_and_login_users import build_user, create_user
from test_get_users import get_user


def update_user(client, id, new_values):
    res = client.put(
        path='/v1/usuarios/' + id,
        data=json.dumps(new_values),
        content_type='application/json'
    )
    return res.status_code, json.loads(res.data.decode())

def test_update_user(client):
    user = build_user(role='host')

    status, res = create_user(client, user)
    user['id'] = res['id']

    new_values = {
        'name': 'newname',
        'surname': 'newsurname',
        'phone': 'newphone',
        'city': 'newcity'
    }
    status, res = update_user(client, user['id'], new_values)

    assert status == 200

    status, updated_user = get_user(client, user['id'])

    for key, value in new_values.items():
        assert updated_user[key] == value
