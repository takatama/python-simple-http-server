import re
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import urlparse
from Hello import Hello

gets = {}

class RequestHandler(BaseHTTPRequestHandler):

    def get(url):
        def _(f):
            gets[url] = f
        return _

    @get('/hello')
    def say(self, query):
        hello = Hello()
        name = query.get('name');
        if name is None:
            return hello.say()
        return hello.say(', '.join(name))

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        path = parsed_path.path
        query = urlparse.parse_qs(parsed_path.query)
        m = re.match(r'/greeting/(\w+)', path)
        if gets.has_key(path):
            message = gets[path](self, query)
        elif bool(m):
            hello = Hello()
            name = m.group(1)
            message = hello.say(name)
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
