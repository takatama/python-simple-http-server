import re
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import urlparse
from Hello import Hello

gets = {}

def get(url):
    def _(f):
        gets[url] = f
    return _

class RequestHandler(BaseHTTPRequestHandler):

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
        for url, func in gets.iteritems():
            print url
            m = re.match(url, path)
            print bool(m)
            if bool(m):
                message = func(self, query)
                self.send_response(200) 
                self.end_headers()
                self.wfile.write(message)
                return

        m = re.match(r'/greeting/(\w+)', path)
        if bool(m):
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
