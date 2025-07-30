import requests

BASE_URL = "https://reqres.in/api"


# 1. GET /users
def test_get_users_returns_200():
    response = requests.get(f"{BASE_URL}/users?page=2")

    assert response.status_code == 200


def test_get_single_user_has_expected_keys():
    response = requests.get(f"{BASE_URL}/users/2")
    body = response.json()

    assert response.status_code == 200
    assert "data" in body
    assert all(key in body["data"] for key in ["id", "email", "first_name", "last_name", "avatar"])


# 2. POST /users
def test_create_user_returns_correct_data():
    name = "morpheus"
    job = "leader"
    response = requests.post(f"{BASE_URL}/users", json={"name": name, "job": job})
    body = response.json()

    assert response.status_code == 200
    assert body["name"] == name
    assert body["job"] == job


def test_create_user_contains_id_and_created_at():
    response = requests.post(f"{BASE_URL}/users", json={"name": "neo", "job": "chosen one"})
    body = response.json()

    assert response.status_code == 200
    assert "id" in body
    assert "createdAt" in body


#  3. PUT /users/{id}
def test_update_user_returns_updated_job():
    new_job = "zion resident"
    response = requests.put(f"{BASE_URL}/users/2", json={"job": new_job})
    body = response.json()

    assert response.status_code == 200
    assert body["job"] == new_job


def test_update_user_contains_updated_at():
    response = requests.put(f"{BASE_URL}/users/2", json={"job": "freed man"})
    body = response.json()

    assert "updatedAt" in body