import requests

BASE_MOCK_URL = "http://0.0.0.0:8000/api"
headers = {"x-api-key": "reqres-free-v1"}


def test_get_second_users_page():
    page = 2
    response = requests.get(f"{BASE_MOCK_URL}/users", params={"page": page})
    body = response.json()

    assert response.status_code == 200
    assert body.get("page") == page
    assert "data" in body
    assert isinstance(body["data"], list)
    assert all(isinstance(user, dict) for user in body["data"])


def test_users_have_expected_keys():
    page = 2
    response = requests.get(f"{BASE_MOCK_URL}/users", params={"page": page})
    body = response.json()

    assert response.status_code == 200
    assert "data" in body
    assert all(
        all(key in user for key in ["id", "email", "first_name", "last_name", "avatar"])
        for user in body["data"]
    )


def test_create_user_returns_correct_data():
    payload = {"name": "morpheus", "job": "leader"}
    response = requests.post(f"{BASE_MOCK_URL}/users", json=payload, headers=headers)
    body = response.json()

    assert response.status_code == 200
    for key, value in payload.items():
        assert body.get(key) == value

    assert "id" in body
    assert "createdAt" in body