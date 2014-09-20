from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from urlparse import urlparse

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200) 
        self.end_headers()
        self.wfile.write("Hello World")
        return

address = ("", 8888)
server = HTTPServer(address, RequestHandler)
server.serve_forever()
