import requests

BASE_MOCK_URL = "http://0.0.0.0:8000/api"
headers = {"x-api-key": "reqres-free-v1"}


def test_get_second_users_page():
    response = requests.get(f"{BASE_MOCK_URL}/users?page=2")
    body = response.json()
    assert body["page"] == 2
    assert response.status_code == 200


def test_get_single_user_has_expected_keys():
    response = requests.get(f"{BASE_MOCK_URL}/users?page=2")
    body = response.json()

    assert response.status_code == 200
    assert "data" in body
    for user in body["data"]:
        for key in ["id", "email", "first_name", "last_name", "avatar"]:
            assert key in user


def test_create_user_returns_correct_data():
    name = "morpheus"
    job = "leader"
    response = requests.post(f"{BASE_MOCK_URL}/users", json={"name": name, "job": job}, headers=headers)
    body = response.json()

    assert response.status_code == 200
    assert body["name"] == name
    assert body["job"] == job