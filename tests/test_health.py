import os
import pytest
import requests

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")


def test_health_returns_ok():
    r = requests.get(f"{BASE_URL}/health/", timeout=10)
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


@pytest.mark.parametrize("path", ["/health/", "/"])
def test_no_server_errors(path):
    r = requests.get(f"{BASE_URL}{path}", timeout=10)
    assert r.status_code < 500, f"{path} returned {r.status_code}"
