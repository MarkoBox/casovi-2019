import json
import pytest


@pytest.mark.usefixtures('client_class')
class TestUsers:

    def test_signup(self):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }
        data = {"username": "Test", "password": "test"}
        url = 'http://127.0.0.1:5000/api/user/register'

        response = self.client.post(url, data=json.dumps(data), headers=headers)

        assert response.status_code == 204
        response = self.client.post(url, data=json.dumps(data), headers=headers)

        assert response.status_code == 400

    def test_login(self):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }
        data = {"username": "Test", "password": "test"}
        url = 'http://127.0.0.1:5000/api/user/login'

        response = self.client.post(url, data=json.dumps(data), headers=headers)

        assert response.content_type == mimetype
        assert response.json['token'] is not None
