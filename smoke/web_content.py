"""Assert that the deployed DevFlow landing page serves real content.

Runs from GitHub Actions so the check is independent of any developer machine.
"""

import os
import sys
import time
import urllib.request

URL = os.environ.get("WEB_URL", "https://devflow-web-agbx.onrender.com/")
ATTEMPTS = 6

CHECKS = [
    ("page title", "DevFlow · team task management"),
    ("hero heading", ">DevFlow<"),
    ("tagline", "task management built in public"),
    ("feature: REST API", "REST API"),
    ("feature: Realtime layer", "Realtime layer"),
    ("feature: Vector search", "Vector search"),
    ("feature: Quality gates", "Quality gates"),
    ("board preview", "board-preview"),
    ("status pills", "status-badge"),
    ("live status probe", "live-status"),
    ("run instructions", "npm run dev"),
    ("footer", "MIT licensed"),
]


def fetch():
    request = urllib.request.Request(URL, headers={"User-Agent": "smoke"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.status, response.read().decode("utf-8", "replace")


def main() -> int:
    html = ""
    status = 0
    for attempt in range(1, ATTEMPTS + 1):
        try:
            status, html = fetch()
            print(f"attempt {attempt} -> HTTP {status} ({len(html)} bytes)")
            if status == 200:
                break
        except Exception as exc:  # noqa: BLE001 - any transport error is retryable
            print(f"attempt {attempt} -> {type(exc).__name__}: {exc}")
        time.sleep(15)
    else:
        print("landing page did not return 200")
        return 1

    failures = [label for label, needle in CHECKS if needle not in html]
    for label, needle in CHECKS:
        print(f"{'PASS' if needle in html else 'FAIL'}  {label}")

    if failures:
        print("missing content: " + ", ".join(failures))
        return 1
    print(f"ALL PASS ({len(CHECKS)} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
