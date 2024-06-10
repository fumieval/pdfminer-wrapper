from pdfminer.high_level import extract_text
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            contentLength = self.headers['Content-Length']
            if contentLength is None:
                raise Exception('Content-Length header is missing')

            content_length = int(contentLength)
            post_data = self.rfile.read(content_length)

            pdf_file = post_data.decode('utf-8')

            text = extract_text(pdf_file)

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(text.encode())
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
