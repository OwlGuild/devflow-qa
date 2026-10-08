import os
import time

import pytest
import requests

RETRIES = 3
RETRY_DELAY_SECONDS = 8
REQUEST_TIMEOUT_SECONDS = 45


def base_url() -> str:
    return os.environ.get("BASE_URL", "http://localhost:8000").rstrip("/")


def fetch(path: str) -> requests.Response:
    """GET with retries so a cold-starting deployment does not fail the suite."""
    url = f"{base_url()}{path}"
    last_exc = None
    for attempt in range(RETRIES):
        try:
            return requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as exc:
            last_exc = exc
            if attempt < RETRIES - 1:
                time.sleep(RETRY_DELAY_SECONDS)
    raise AssertionError(f"{url} unreachable after {RETRIES} attempts: {last_exc}") from last_exc


def test_health_returns_ok():
    r = fetch("/health/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


@pytest.mark.parametrize("path", ["/health/", "/"])
def test_no_server_errors(path):
    r = fetch(path)
    assert r.status_code < 500, f"{path} returned {r.status_code}"
