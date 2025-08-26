import json
from http import HTTPStatus
from pathlib import Path

import pytest
from app.models.User import User


@pytest.fixture(scope="module")
def fill_test_data(api_mock_client):
    """Создаём пользователей из users.json и удаляем после модуля."""
    data_path = Path(__file__).resolve().parent.parent / "users.json"
    with data_path.open(encoding="utf-8") as f:
        test_data_users = json.load(f)

    api_users = []
    for user in test_data_users:
        resp = api_mock_client.create_user(user)
        api_users.append(resp.json())

    user_ids = [u["id"] for u in api_users]

    yield user_ids

    for user_id in user_ids:
        api_mock_client.delete_user(user_id)


@pytest.fixture
def users(api_mock_client):
    resp = api_mock_client.get_list_users()
    assert resp.status_code == HTTPStatus.OK
    return resp.json()


@pytest.mark.usefixtures("fill_test_data")
def test_users(api_mock_client):
    resp = api_mock_client.get_list_users()
    assert resp.status_code == HTTPStatus.OK

    for user in resp.json():
        User.model_validate(user)


@pytest.mark.usefixtures("fill_test_data")
def test_users_no_duplicates(users):
    users_ids = [user["id"] for user in users]
    assert len(users_ids) == len(set(users_ids))


def test_user(api_mock_client, fill_test_data):
    for user_id in (fill_test_data[0], fill_test_data[-1]):
        resp = api_mock_client.get_user(user_id)
        assert resp.status_code == HTTPStatus.OK
        User.model_validate(resp.json())


@pytest.mark.parametrize("user_id", [13])
def test_user_nonexistent_values(api_mock_client, user_id):
    resp = api_mock_client.get_user(user_id)
    assert resp.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
def test_user_invalid_values(api_mock_client, user_id):
    resp = api_mock_client.get_user(user_id)
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.fixture
def new_user_data():
    data_path = Path(__file__).resolve().parent.parent / "users.json"
    with data_path.open(encoding="utf-8") as f:
        users = json.load(f)
    return users[0]


def test_create_user(api_mock_client, new_user_data):
    resp = api_mock_client.create_user(new_user_data)
    assert resp.status_code == HTTPStatus.CREATED

    user = resp.json()
    User.model_validate(user)

    api_mock_client.delete_user(user["id"])


def test_delete_user(api_mock_client, new_user_data):
    created = api_mock_client.create_user(new_user_data).json()
    delete_resp = api_mock_client.delete_user(created["id"])
    assert delete_resp.status_code in (HTTPStatus.NO_CONTENT, HTTPStatus.OK)

    check = api_mock_client.get_user(created["id"])
    assert check.status_code == HTTPStatus.NOT_FOUND


def test_patch_user(api_mock_client, new_user_data):
    created = api_mock_client.create_user(new_user_data).json()

    patch_payload = {"first_name": "Updated"}
    patch_resp = api_mock_client.patch_user(created["id"], patch_payload)
    assert patch_resp.status_code == HTTPStatus.OK

    updated = patch_resp.json()
    assert updated["first_name"] == "Updated"

    api_mock_client.delete_user(created["id"])