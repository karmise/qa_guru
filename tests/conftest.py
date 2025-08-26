import os

import dotenv
import pytest

from app.ApiMockClient import ApiMockClient


@pytest.fixture(scope="session", autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope="session")
def app_url():
    return os.getenv("APP_URL")


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="local",
        choices=["local", "docker", "compose"],
        help="Выбор окружения: local/docker/compose",
    )


ENV_URLS = {
    "local": os.getenv("APP_URL", "http://127.0.0.1:8002"),
    "docker": "http://127.0.0.1:8002",
    "compose": "http://127.0.0.1:8002",
}


@pytest.fixture(scope="session")
def env_name(pytestconfig):
    return pytestconfig.getoption("--env")


@pytest.fixture(scope="session")
def base_url(env_name):
    return ENV_URLS[env_name]


@pytest.fixture(scope="session")
def api_mock_client(base_url):
    return ApiMockClient(base_url)
