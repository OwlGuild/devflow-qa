import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest
from dotenv import load_dotenv

load_dotenv()


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health/":
            payload = {"status": "ok", "service": "devflow-qa"}
            code = 200
        elif self.path == "/":
            payload = {"status": "ok"}
            code = 200
        else:
            payload = {"detail": "not found"}
            code = 404
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args):
        pass


@pytest.fixture(scope="session", autouse=True)
def live_server():
    """Default BASE_URL to a local fixture, but never override an explicit target."""
    if os.environ.get("BASE_URL"):
        yield
        return

    server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    os.environ["BASE_URL"] = "http://127.0.0.1:{}".format(server.server_address[1])
    yield
    server.shutdown()
