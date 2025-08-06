from http import HTTPStatus

import requests

from homework_1.models.user import User

headers = {"x-api-key": "reqres-free-v1"}


def test_get_second_users_page(app_url):
    page = 2
    response = requests.get(f"{app_url}/api/users", params={"page": page})
    users = response.json()

    for user in users:
        User.model_validate(user)

    assert response.status_code == HTTPStatus.OK
    assert isinstance(users, list)
    assert all(isinstance(user, dict) for user in users)


def test_users_endpoint_returns_list(app_url):
    response = requests.get(f"{app_url}/api/users")
    body = response.json()

    assert response.status_code == HTTPStatus.OK
    assert isinstance(body, list)
    assert body, "Список пользователей пустой"


def test_create_user_returns_correct_data(app_url):
    payload = {"name": "morpheus", "job": "leader"}
    response = requests.post(f"{app_url}/api/users", json=payload, headers=headers)
    body = response.json()

    assert response.status_code == HTTPStatus.OK
    for key, value in payload.items():
        assert body.get(key) == value

    assert "id" in body
    assert "createdAt" in body