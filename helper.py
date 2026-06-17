#!/usr/bin/env python3
"""
Folder Tree Helper
Lets Ctrl+click open files and folders with their default apps.
Keep this window open while using Folder Tree in your browser.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
import subprocess
import os
import sys

PORT = 7432


class Handler(BaseHTTPRequestHandler):

    def respond(self, code, body=b'OK'):
        self.send_response(code)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        # CORS preflight — needed when called from GitHub Pages (HTTPS)
        self.respond(200)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == '/ping':
            self.respond(200, b'pong')

        elif parsed.path == '/open':
            params = parse_qs(parsed.query)
            path = unquote(params.get('path', [''])[0])

            if not path:
                self.respond(400, b'Missing path')
                return

            if not os.path.exists(path):
                self.respond(404, b'Path not found on this machine')
                return

            try:
                if os.path.isdir(path):
                    # Open folder in Windows Explorer
                    subprocess.Popen(['explorer', path])
                else:
                    # Open file with its default application (same as double-clicking)
                    os.startfile(path)
                self.respond(200, b'OK')
            except Exception as e:
                self.respond(500, str(e).encode())

        else:
            self.respond(404, b'Unknown endpoint')

    def log_message(self, fmt, *args):
        pass  # suppress per-request noise in the console


if __name__ == '__main__':
    try:
        server = HTTPServer(('localhost', PORT), Handler)
    except OSError:
        print(f'\nPort {PORT} is already in use — is the helper already running?')
        input('Press Enter to exit.')
        sys.exit(1)

    print('┌──────────────────────────────────────────┐')
    print('│  Folder Tree Helper                      │')
    print('├──────────────────────────────────────────┤')
    print(f'│  Listening on http://localhost:{PORT}     │')
    print('│  Keep this window open while browsing    │')
    print('│  Press Ctrl+C to stop                    │')
    print('└──────────────────────────────────────────┘\n')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nHelper stopped.')
