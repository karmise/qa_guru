import requests
from http import HTTPStatus


def test_pagination_returns_expected_page_size(app_url):
    page_size = 5
    response = requests.get(f"{app_url}/api/users", params={"size": page_size, "page": 1})

    assert response.status_code == HTTPStatus.OK
    body = response.json()
    assert "items" in body
    assert len(body["items"]) == page_size


def test_pagination_total_pages_changes_with_size(app_url):
    response_small = requests.get(f"{app_url}/api/users", params={"size": 3})
    response_large = requests.get(f"{app_url}/api/users", params={"size": 6})

    body_small = response_small.json()
    body_large = response_large.json()

    assert body_small["pages"] > body_large["pages"]


def test_pagination_returns_different_data_on_different_pages__(app_url):
    response_page1 = requests.get(f"{app_url}/api/users", params={"size": 3, "page": 1})
    response_page2 = requests.get(f"{app_url}/api/users", params={"size": 3, "page": 2})

    items_page1 = [user["id"] for user in response_page1.json()["items"]]
    items_page2 = [user["id"] for user in response_page2.json()["items"]]

    assert items_page1 != items_page2