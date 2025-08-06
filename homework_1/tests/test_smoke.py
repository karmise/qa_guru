from http import HTTPStatus

import requests


def test_status_endpoint(app_url):
    response = requests.get(f"{app_url}/status")
    body = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "users" in body
    assert isinstance(body["users"], bool)


def test_smoke_get_users(app_url):
    response = requests.get(f"{app_url}/api/users")
    assert response.status_code == HTTPStatus.OK


def test_smoke_get_user_by_id(app_url):
    response = requests.get(f"{app_url}/api/users/1")
    assert response.status_code in (HTTPStatus.OK, HTTPStatus.NOT_FOUND)