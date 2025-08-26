import requests


class ApiMockClient:

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def get_status(self):
        return self.session.get(self._url("/status"))

    def get_list_users(self):
        return self.session.get(self._url("/api/users/"))

    def create_user(self, payload: dict):
        return self.session.post(self._url("/api/users/"), json=payload)

    def get_user(self, user_id: int | str):
        return self.session.get(self._url(f"/api/users/{user_id}"))

    def patch_user(self, user_id: int | str, payload: dict):
        return self.session.patch(self._url(f"/api/users/{user_id}"), json=payload)

    def delete_user(self, user_id: int | str):
        return self.session.delete(self._url(f"/api/users/{user_id}"))