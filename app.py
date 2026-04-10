from __future__ import annotations

import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from marketplace_service import MarketplaceService

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"


class DashboardHandler(BaseHTTPRequestHandler):
    service = MarketplaceService(BASE_DIR / "data" / "sample_marketplace_mac.json")

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/":
            return self._send_file(STATIC_DIR / "index.html", "text/html; charset=utf-8")
        if parsed.path.startswith("/static/"):
            rel_path = parsed.path.replace("/static/", "", 1)
            file_path = STATIC_DIR / rel_path
            mime = "text/plain; charset=utf-8"
            if rel_path.endswith(".css"):
                mime = "text/css; charset=utf-8"
            elif rel_path.endswith(".js"):
                mime = "application/javascript; charset=utf-8"
            return self._send_file(file_path, mime)
        if parsed.path == "/api/marketplace":
            return self._send_marketplace_data(parsed.query)

        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def _send_marketplace_data(self, query_string: str) -> None:
        query = parse_qs(query_string).get("query", ["mac"])[0].strip() or "mac"
        data = self.service.search(query=query, limit=10)
        payload = {
            "query": query,
            "count": len(data),
            "source": "facebook_marketplace_sample",
            "items": data,
        }
        body = json.dumps(payload).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: Path, content_type: str) -> None:
        if not path.exists() or not path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return
        body = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run() -> None:
    port = int(os.getenv("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), DashboardHandler)
    print(f"Dashboard running on http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
