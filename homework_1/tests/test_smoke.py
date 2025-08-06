from http import HTTPStatus

import requests


def test_status_endpoint(app_url):
    response = requests.get(f"{app_url}/api/status")
    body = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "users" in body
    assert isinstance(body["users"], bool)