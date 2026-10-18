"""Tiny local launcher/server for Little Wilds. No packages required."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse
import json
import os
import webbrowser

ROOT = Path(__file__).resolve().parent
MODS = (ROOT / "Modifications").resolve()
HOST = "127.0.0.1"
PORT = 8135


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/modifications":
            return self.send_json(MODS / "manifest.json")
        if path.startswith("/api/mod/"):
            folder = unquote(path[len("/api/mod/"):]).strip("/")
            # Folder names are one path segment; reject traversal and hidden folders.
            if not folder or folder in {".", ".."} or "/" in folder or "\\" in folder:
                self.send_error(400, "Invalid mod folder name")
                return
            candidate = (MODS / folder / "mod.json").resolve()
            if MODS not in candidate.parents:
                self.send_error(403, "Mod path is outside the Modifications folder")
                return
            return self.send_json(candidate)
        return super().do_GET()

    def send_json(self, path):
        try:
            body = path.read_bytes()
            json.loads(body)
        except FileNotFoundError:
            self.send_error(404, "Mod manifest or mod.json was not found")
            return
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.send_error(422, "JSON file is invalid")
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    os.chdir(ROOT)
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    # "localhost" is usually excluded from browser proxy settings, unlike an
    # explicit loopback address on some Windows configurations.
    url = f"http://localhost:{PORT}"
    print(f"Little Wilds is ready at {url}")
    print("Keep this window open while playing. Press Ctrl+C to stop.")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
