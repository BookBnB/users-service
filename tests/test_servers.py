import json
from base64 import b64decode


def build_server(nombre='un nombre'):
    return {
        'nombre': nombre
    }


def create_server(client, data_dict):
    res = client.post(path='/v1/servidores', data=json.dumps(data_dict), content_type='application/json')
    return res.status_code, json.loads(res.data.decode())


def validate_create_server_response(status, res, nombre):
    assert status == 201
    assert res['id']
    assert res['token']
    assert res['nombre'] == nombre


def validate_same_server(server, res):
    assert res['id']
    assert res['token']
    assert res['nombre'] == server['nombre']


def test_create_server(client):
    user = build_server(nombre='un nombre')

    status, res = create_server(client, user)

    validate_create_server_response(status, res, 'un nombre')


def test_create_server_without_name(client):
    user = {}

    status, res = create_server(client, user)

    assert status == 400
    assert res['message'] == 'Missing server nombre'


def test_create_and_list_servers(client):
    server1 = build_server('un nombre')
    server2 = build_server('otro nombre')
    create_server(client, server1)
    create_server(client, server2)

    res = client.get(path='/v1/servidores')

    servers_array = json.loads(res.data.decode())

    assert len(servers_array) == 2
    validate_same_server(server1, servers_array[0])
    validate_same_server(server2, servers_array[1])
