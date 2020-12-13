import json
import vcr

def test_create_user_expired_token(client):
    with vcr.use_cassette('tests/vcr_cassettes/expired_token.yaml'):
        user = {
            'token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ0Y2JhMjVlNTYzNjYwYTkwMDlkODIwYTFjMDIwMjIwNzA1NzRlODIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI3MzgyNzY0ODI1ODEtOTFjODZkYmk4ZGdxOXJvYmZja2ZscWQ4cTB0c3U4Z3QuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI3MzgyNzY0ODI1ODEtN3BoczFvajMxcHBsdmgybjVjODdkMTVtZm9zMjc5MXUuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTE4NDkzOTU2NjMzMjgwMzg5MDUiLCJoZCI6ImZpLnViYS5hciIsImVtYWlsIjoiZmZ1c2Fyb0BmaS51YmEuYXIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IkZyYW5jbyBGdXNhcm8iLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EtL0FPaDE0R2d5WERPcHQxWTVlVVJXUEJzZ3RzVVZxU0JzMlBLR1VPcU0yV2RzPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IkZyYW5jbyIsImZhbWlseV9uYW1lIjoiRnVzYXJvIiwibG9jYWxlIjoiZXMiLCJpYXQiOjE2MDc2MTM1NDksImV4cCI6MTYwNzYxNzE0OX0.RHRP2yCScys5xwszr98ipmUsUoFMBXlSUMPpGoJEChI6NRbK8K1b0StE1FZ_VPAeEdc7x3YZ037QYQz7xR5daRe1umIOGdohxkqdKaadHrr6VSoN6Hm329244LE8uSq1fvDgyHjPnnZtOGmhoHLCIyP1V1760i8XJxg8k6Tfgl5UPfis8FtlKKAkrKG7unosccjBixZFsI7C3wlr9gQpGnzn8Lh0CpZc8JqXzMe1Qezz_cJCVr_TuE0RvBNhsTGaYHhiKcPAKem_ehen5HFtk5jqiMtJYEWTsXF2kRB8LSuakg4rd9FpIBsqWiYS-ZswxIVB5j-s2Q7mqHVxjcjPEQ',
            'role': 'host'
        }
        res = client.post(path='/v1/usuarios/google', data=json.dumps(user), content_type='application/json')
        parsed_res = json.loads(res.data.decode())

        assert res.status_code == 400
        assert 'TokenError' == parsed_res['error']
        assert 'Token expired' in parsed_res['message']
