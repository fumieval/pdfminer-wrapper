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

            # Input type is always application/pdf
            # determine the output format from the Accept header
            # if Accept header is not present, default to text/plain
            format = 'text'
            if 'Accept' in self.headers:
                if 'text/plain' in self.headers['Accept']:
                    format = 'text'
                elif 'text/html' in self.headers['Accept']:
                    format = 'html'

            post_data = self.rfile.read(content_length)

            pdf_file = post_data.decode('utf-8')

            outfp = StringIO()
            extract_text_to_fp(pdf_file, output_type=format, outfp=outfp)

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(outfp.getvalue().encode())
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
