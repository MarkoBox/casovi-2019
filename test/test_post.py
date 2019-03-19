import pytest
from flask import url_for
import json


@pytest.mark.usefixtures('client_class')
class TestPosts:

    def test_app(self):
        assert self.client.get('http://127.0.0.1:5000/api/posts/').status_code == 200

    def test_get_single_post(self):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }
        url = 'http://127.0.0.1:5000/api/posts/1'

        response = self.client.get(url, headers=headers)

        assert response.status_code == 200
        assert response.json['id'] == 1

    def test_limit_offset(self):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }
        query_string = {"limit": "2"}
        url = 'http://127.0.0.1:5000/api/posts/'

        response = self.client.get(url, headers=headers, query_string=query_string)

        assert response.status_code == 200
        assert len(response.json) == 2
        query_string = {"limit": "1"}
        url = 'http://127.0.0.1:5000/api/posts/'

        response = self.client.get(url, headers=headers, query_string=query_string)

        assert response.status_code == 200
        assert len(response.json) == 1
