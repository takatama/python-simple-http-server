from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import urlparse
from urllib.parse import parse_qs
import re
from Hello import Hello

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)
        m = re.match(r'/greeting/(\w+)', path)
        if bool(m):
            hello = Hello()
            name = m.group(1)
            message = hello.say(name)
        elif path == '/hello':
            hello = Hello()
            name = query.get('name');
            if name is None:
                message = hello.say()
            else:
                message = hello.say(', '.join(name))
        else:
            self.send_response(404) 
            self.end_headers()
            self.wfile.write(bytes('404 Not Found','UTF-8'))
            return
        self.send_response(200) 
        self.end_headers()
        self.wfile.write(bytes(message, 'UTF-8'))
        return

address = ('', 8888)
server = HTTPServer(address, RequestHandler)
server.serve_forever()
