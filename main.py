import pdfplumber
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
import os
import json
import utils

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            contentLength = self.headers['Content-Length']
            if contentLength is None:
                raise Exception('Content-Length header is missing')

            content_length = int(contentLength)

            post_data = self.rfile.read(content_length)

            with pdfplumber.open(BytesIO(post_data)) as pdf:
                resp = utils.to_markdown(pdf)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                for chunk in resp:
                    self.wfile.write((chunk + "\n").encode())
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(str(e).encode())

# Read the port from the PORT environment variable
port = int(os.environ.get('PORT', 8080))

# Create an instance of the HTTP server
httpd = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)

# Print the log as JSON
print(json.dumps({"level": "info", "message": f"listening on port {port}"}))

# Start the server
httpd.serve_forever()
