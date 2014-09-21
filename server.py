from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from urlparse import urlparse
from Hello import Hello

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if (self.path == '/hello'):
            hello = Hello()
            response = hello.say()
        else:
            self.send_response(404) 
            self.end_headers()
            self.wfile.write("404 Not Found")
            return
        self.send_response(200) 
        self.end_headers()
        self.wfile.write(response)
        return

address = ("", 8888)
server = HTTPServer(address, RequestHandler)
server.serve_forever()
