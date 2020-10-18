def test_home(client):
    res = client.get('/v1/')
    assert res.data == b'{"hello":"world"}\n'
