import json
from base64 import b64decode


def build_server(nombre='un nombre'):
    return {
        'nombre': nombre
    }


def create_server(client, data_dict):
    res = client.post(path='/v1/servidores', data=json.dumps(data_dict), content_type='application/json')
    return res.status_code, json.loads(res.data.decode())


def block_server(client, server, blocked = True):
    body = {
        'bloqueado': blocked
    }

    res = client.put(
        path='/v1/servidores/' + server['nombre'] + '/bloqueo',
        data=json.dumps(body),
        content_type='application/json'
    )

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


def test_server_request_missing_token(app, client):
    app.config['REQUIRE_API_KEY'] = True

    server = build_server(nombre='un nombre')
    status, res = create_server(client, server)

    res = client.get(path='/v1/usuarios')

    assert res.status_code == 403
    assert res.get_json()['message'] == 'Missing API key'


def test_server_request_valid_token(app, client):
    app.config['REQUIRE_API_KEY'] = True

    server = build_server(nombre='un nombre')
    status, res = create_server(client, server)

    res = client.get(
        path='/v1/usuarios',
        headers=[('x-api-key', res['token'])]
    )

    assert res.status_code == 200


def test_server_request_invalid_token(app, client):
    app.config['REQUIRE_API_KEY'] = True

    server = build_server(nombre='un nombre')
    status, res = create_server(client, server)

    res = client.get(
        path='/v1/usuarios',
        headers=[('x-api-key', 'aninvalidtoken')]
    )

    assert res.status_code == 403
    assert res.get_json()['message'] == 'Invalid API key'


def test_block_server(app, client):
    server = build_server(nombre='un nombre')
    status, res = create_server(client, server)

    status, res = block_server(client, server)

    assert status == 200


def test_server_request_blocked_token(app, client):
    app.config['REQUIRE_API_KEY'] = True

    server = build_server(nombre='un nombre')
    status, res = create_server(client, server)
    token = res['token']
    status, res = block_server(client, server)

    res = client.get(
        path='/v1/usuarios',
        headers=[('x-api-key', token)]
    )

    assert res.status_code == 403
    assert res.get_json()['message'] == 'Blocked API key'


def test_server_request_unblocked_token(app, client):
    app.config['REQUIRE_API_KEY'] = True

    server = build_server(nombre='un nombre')
    status, res = create_server(client, server)
    token = res['token']
    status, res = block_server(client, server)
    status, res = block_server(client, server, blocked=False)

    res = client.get(
        path='/v1/usuarios',
        headers=[('x-api-key', token)]
    )

    assert res.status_code == 200
