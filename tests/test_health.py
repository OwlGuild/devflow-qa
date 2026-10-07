import os
import pytest
import requests


def base_url() -> str:
    return os.environ.get("BASE_URL", "http://localhost:8000").rstrip("/")


def test_health_returns_ok():
    r = requests.get(f"{base_url()}/health/", timeout=10)
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


@pytest.mark.parametrize("path", ["/health/", "/"])
def test_no_server_errors(path):
    r = requests.get(f"{base_url()}{path}", timeout=10)
    assert r.status_code < 500, f"{path} returned {r.status_code}"
