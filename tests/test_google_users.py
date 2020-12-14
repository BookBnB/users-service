import json
import vcr
from freezegun import freeze_time
from base64 import b64decode

def create_user(client, token):
    with vcr.use_cassette('tests/vcr_cassettes/google_token_certificate.yaml'):
        user = {
            'token': token,
            'role': 'host'
        }
        res = client.post(path='/v1/usuarios/google', data=json.dumps(user), content_type='application/json')
        return res.status_code, json.loads(res.data.decode())

@freeze_time("2020-12-14 00:00:00Z")
def test_create_user_expired_token(client):
    status, res = create_user(client, 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ0Y2JhMjVlNTYzNjYwYTkwMDlkODIwYTFjMDIwMjIwNzA1NzRlODIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI3MzgyNzY0ODI1ODEtOTFjODZkYmk4ZGdxOXJvYmZja2ZscWQ4cTB0c3U4Z3QuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI3MzgyNzY0ODI1ODEtN3BoczFvajMxcHBsdmgybjVjODdkMTVtZm9zMjc5MXUuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTE4NDkzOTU2NjMzMjgwMzg5MDUiLCJoZCI6ImZpLnViYS5hciIsImVtYWlsIjoiZmZ1c2Fyb0BmaS51YmEuYXIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IkZyYW5jbyBGdXNhcm8iLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EtL0FPaDE0R2d5WERPcHQxWTVlVVJXUEJzZ3RzVVZxU0JzMlBLR1VPcU0yV2RzPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IkZyYW5jbyIsImZhbWlseV9uYW1lIjoiRnVzYXJvIiwibG9jYWxlIjoiZXMiLCJpYXQiOjE2MDc2MTM1NDksImV4cCI6MTYwNzYxNzE0OX0.RHRP2yCScys5xwszr98ipmUsUoFMBXlSUMPpGoJEChI6NRbK8K1b0StE1FZ_VPAeEdc7x3YZ037QYQz7xR5daRe1umIOGdohxkqdKaadHrr6VSoN6Hm329244LE8uSq1fvDgyHjPnnZtOGmhoHLCIyP1V1760i8XJxg8k6Tfgl5UPfis8FtlKKAkrKG7unosccjBixZFsI7C3wlr9gQpGnzn8Lh0CpZc8JqXzMe1Qezz_cJCVr_TuE0RvBNhsTGaYHhiKcPAKem_ehen5HFtk5jqiMtJYEWTsXF2kRB8LSuakg4rd9FpIBsqWiYS-ZswxIVB5j-s2Q7mqHVxjcjPEQ')
    assert status == 400
    assert 'TokenError' == res['error']
    assert 'Token expired' in res['message']

def test_create_user_invalid_token(client):
    for token in ['s.s.s', 'a.b.c']:
        status, res = create_user(client, token)

        assert status == 400
        assert 'TokenError' == res['error']
        assert 'Invalid base64-encoded string' in res['message']

@freeze_time("2020-12-14 00:00:00Z")
def test_create_user_valid(client):
    status, res = create_user(client, 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImUxOTdiZjJlODdiZDE5MDU1NzVmOWI2ZTVlYjQyNmVkYTVkNTc0ZTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTEwNjAyMDg1MDMxOTkzNTE2MTAiLCJoZCI6ImZpLnViYS5hciIsImVtYWlsIjoic2JsYXpxdWV6QGZpLnViYS5hciIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoibThhVV9KOFJydFEtUTk4NnNLWEgwQSIsIm5hbWUiOiJTZWJhc3Rpw6FuIEFsZWphbmRybyBCbMOhenF1ZXogT2xpdmVyYSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS0vQU9oMTRHaTBTTEk3QWtzenVOWHNtd19FcnV0cnFldjRxSFNDTUpwZlMwbk49czk2LWMiLCJnaXZlbl9uYW1lIjoiU2ViYXN0acOhbiBBbGVqYW5kcm8iLCJmYW1pbHlfbmFtZSI6IkJsw6F6cXVleiBPbGl2ZXJhIiwibG9jYWxlIjoiZXMiLCJpYXQiOjE2MDc5MDM4MjIsImV4cCI6MTYwNzkwNzQyMn0.B7DOtaUKDFfKPyTugsAep8kCsXXl6S7QIux53K5DiYC9qKx37cP3kSN09h1mm6k-XPIKBnkng6NTEAafhzCvYUKF2grcyhQQpXkK-RR-hlbpn0KomShN6xzQiQYWpTXAjGAE9g-2ukHWO2MoWTudLFwV1mHBTQl2FnEwJ_QYdrZh_Kkdq-6-ycZJxW12LvH3n6lyGawIUN2ZizWjU8wiv5cs3YHgZYvwe0ufI9e8RoYVSwfb2dmSx_PH5Quo7I8EsIqcnNQQjlWZ48Ko3jQcYSKkdPMutxctuePTDggXI3cNZZLoaXla7QVrqrHUtfxjAQdqKn1cP3cyaKXYnXvjZQ')

    assert status == 200
    assert res['id']
    assert res['email'] == 'sblazquez@fi.uba.ar'
    assert res['name'] == 'Sebastián Alejandro'
    assert res['surname'] == 'Blázquez Olivera'

@freeze_time("2020-12-14 00:00:00Z")
def test_login(client):
    create_user(client, 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImUxOTdiZjJlODdiZDE5MDU1NzVmOWI2ZTVlYjQyNmVkYTVkNTc0ZTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTEwNjAyMDg1MDMxOTkzNTE2MTAiLCJoZCI6ImZpLnViYS5hciIsImVtYWlsIjoic2JsYXpxdWV6QGZpLnViYS5hciIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoibThhVV9KOFJydFEtUTk4NnNLWEgwQSIsIm5hbWUiOiJTZWJhc3Rpw6FuIEFsZWphbmRybyBCbMOhenF1ZXogT2xpdmVyYSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS0vQU9oMTRHaTBTTEk3QWtzenVOWHNtd19FcnV0cnFldjRxSFNDTUpwZlMwbk49czk2LWMiLCJnaXZlbl9uYW1lIjoiU2ViYXN0acOhbiBBbGVqYW5kcm8iLCJmYW1pbHlfbmFtZSI6IkJsw6F6cXVleiBPbGl2ZXJhIiwibG9jYWxlIjoiZXMiLCJpYXQiOjE2MDc5MDM4MjIsImV4cCI6MTYwNzkwNzQyMn0.B7DOtaUKDFfKPyTugsAep8kCsXXl6S7QIux53K5DiYC9qKx37cP3kSN09h1mm6k-XPIKBnkng6NTEAafhzCvYUKF2grcyhQQpXkK-RR-hlbpn0KomShN6xzQiQYWpTXAjGAE9g-2ukHWO2MoWTudLFwV1mHBTQl2FnEwJ_QYdrZh_Kkdq-6-ycZJxW12LvH3n6lyGawIUN2ZizWjU8wiv5cs3YHgZYvwe0ufI9e8RoYVSwfb2dmSx_PH5Quo7I8EsIqcnNQQjlWZ48Ko3jQcYSKkdPMutxctuePTDggXI3cNZZLoaXla7QVrqrHUtfxjAQdqKn1cP3cyaKXYnXvjZQ')

    with vcr.use_cassette('tests/vcr_cassettes/google_token_certificate.yaml'):
        res = client.post(path='/v1/sesiones/google', data=json.dumps({
            'token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImUxOTdiZjJlODdiZDE5MDU1NzVmOWI2ZTVlYjQyNmVkYTVkNTc0ZTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTEwNjAyMDg1MDMxOTkzNTE2MTAiLCJoZCI6ImZpLnViYS5hciIsImVtYWlsIjoic2JsYXpxdWV6QGZpLnViYS5hciIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoibThhVV9KOFJydFEtUTk4NnNLWEgwQSIsIm5hbWUiOiJTZWJhc3Rpw6FuIEFsZWphbmRybyBCbMOhenF1ZXogT2xpdmVyYSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS0vQU9oMTRHaTBTTEk3QWtzenVOWHNtd19FcnV0cnFldjRxSFNDTUpwZlMwbk49czk2LWMiLCJnaXZlbl9uYW1lIjoiU2ViYXN0acOhbiBBbGVqYW5kcm8iLCJmYW1pbHlfbmFtZSI6IkJsw6F6cXVleiBPbGl2ZXJhIiwibG9jYWxlIjoiZXMiLCJpYXQiOjE2MDc5MDM4MjIsImV4cCI6MTYwNzkwNzQyMn0.B7DOtaUKDFfKPyTugsAep8kCsXXl6S7QIux53K5DiYC9qKx37cP3kSN09h1mm6k-XPIKBnkng6NTEAafhzCvYUKF2grcyhQQpXkK-RR-hlbpn0KomShN6xzQiQYWpTXAjGAE9g-2ukHWO2MoWTudLFwV1mHBTQl2FnEwJ_QYdrZh_Kkdq-6-ycZJxW12LvH3n6lyGawIUN2ZizWjU8wiv5cs3YHgZYvwe0ufI9e8RoYVSwfb2dmSx_PH5Quo7I8EsIqcnNQQjlWZ48Ko3jQcYSKkdPMutxctuePTDggXI3cNZZLoaXla7QVrqrHUtfxjAQdqKn1cP3cyaKXYnXvjZQ',
        }), content_type='application/json')

    base64_data = res.get_json()['token'].split('.')[1]

    missing_padding = len(base64_data) % 4
    if missing_padding:
        base64_data += (b'='* (4 - missing_padding)).decode()

    decoded_data = b64decode(base64_data.encode()).decode()
    data = json.loads(decoded_data)

    assert res.status_code == 200
    assert data['id']
    assert data['email'] == 'sblazquez@fi.uba.ar'
    assert data['role'] == 'host'
    assert data['exp']
