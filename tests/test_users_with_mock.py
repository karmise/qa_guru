import json
from http import HTTPStatus

import pytest
from pathlib import Path
import requests
from app.models.User import User


@pytest.fixture(scope="module")
def fill_test_data(app_url):
    data_path = Path(__file__).resolve().parent.parent / "users.json"

    with data_path.open(encoding="utf-8") as f:
        test_data_users = json.load(f)

    api_users = []
    for user in test_data_users:
        response = requests.post(f"{app_url}/api/users/", json=user)
        api_users.append(response.json())

    user_ids = [user["id"] for user in api_users]

    yield user_ids

    for user_id in user_ids:
        requests.delete(f"{app_url}/api/users/{user_id}")


@pytest.fixture
def users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()


@pytest.fixture
def new_user_data():
    data_path = Path(__file__).resolve().parent.parent / "users.json"
    with data_path.open(encoding="utf-8") as f:
        users = json.load(f)
    return users[0]


@pytest.mark.usefixtures("fill_test_data")
def test_users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK

    user_list = response.json()
    for user in user_list:
        User.model_validate(user)


@pytest.mark.usefixtures("fill_test_data")
def test_users_no_duplicates(users):
    users_ids = [user["id"] for user in users]
    assert len(users_ids) == len(set(users_ids))


def test_user(app_url, fill_test_data):
    for user_id in (fill_test_data[0], fill_test_data[-1]):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK
        user = response.json()
        User.model_validate(user)


@pytest.mark.parametrize("user_id", [13])
def test_user_nonexistent_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
def test_user_invalid_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


#  post
def test_create_user(app_url, new_user_data):
    response = requests.post(f"{app_url}/api/users/", json=new_user_data)
    assert response.status_code == HTTPStatus.CREATED

    user = response.json()
    User.model_validate(user)

    requests.delete(f"{app_url}/api/users/{user['id']}")


# delete
def test_delete_user(app_url, new_user_data):
    create_response = requests.post(f"{app_url}/api/users/", json=new_user_data)
    assert create_response.status_code == HTTPStatus.CREATED
    user = create_response.json()

    delete_response = requests.delete(f"{app_url}/api/users/{user['id']}")
    assert delete_response.status_code == HTTPStatus.OK

    get_response = requests.get(f"{app_url}/api/users/{user['id']}")
    assert get_response.status_code == HTTPStatus.NOT_FOUND


# patch
def test_patch_user(app_url, new_user_data):
    create_response = requests.post(f"{app_url}/api/users/", json=new_user_data)
    assert create_response.status_code == HTTPStatus.CREATED
    user = create_response.json()

    updated_data = {"first_name": "Updated Name"}
    patch_response = requests.patch(f"{app_url}/api/users/{user['id']}", json=updated_data)
    assert patch_response.status_code == HTTPStatus.OK

    updated_user = patch_response.json()
    assert updated_user["first_name"] == updated_data["first_name"]

    requests.delete(f"{app_url}/api/users/{user['id']}")