import os, socket
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        msg = f'{{"status": "ok", "container_id": "{socket.gethostname()}"}}'
        self.wfile.write(msg.encode())

HTTPServer(('0.0.0.0', 5000), Handler).serve_forever()
