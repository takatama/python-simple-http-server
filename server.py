from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import urlparse
from Hello import Hello

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        path = parsed_path.path
        query = urlparse.parse_qs(parsed_path.query)
        if (path == '/hello'):
            hello = Hello()
            name = query.get('name');
            if name is None:
                message = hello.say()
            else:
                message = hello.say(', '.join(name))
        else:
            self.send_response(404) 
            self.end_headers()
            self.wfile.write('404 Not Found')
            return
        self.send_response(200) 
        self.end_headers()
        self.wfile.write(message)
        return

address = ('', 8888)
server = HTTPServer(address, RequestHandler)
server.serve_forever()
