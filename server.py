import re
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from Hello import Hello

gets = {}

def get(url):
    def _(f):
        url_pattern = ''
        params = []
        url_list = url.split('/')
        url_list.pop(0)
        for u in url_list:
            if u.find(':') == 0:
               params.append(u.replace(':', ''))
               u = '(\w+)'
            url_pattern += '/' + u
        gets[url_pattern] = f
    return _

class RequestHandler(BaseHTTPRequestHandler):

    @get('/hello')
    def say(self, query, *args):
        hello = Hello()
        name = query.get('name');
        if name is None:
            return hello.say()
        return hello.say(', '.join(name))

    @get('/greeting/:name')
    def greeting(self, query, *args):
        hello = Hello()
        return hello.say(args[0])

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        path = parsed_path.path
        query = urlparse.parse_qs(parsed_path.query)
        for url, func in gets.iteritems():
            m = re.match(url, path)
            if bool(m):
                message = func(self, query, *m.groups())
                self.send_response(200) 
                self.end_headers()
                self.wfile.write(message)
                return
        self.send_response(404) 
        self.end_headers()
        self.wfile.write('404 Not Found')

address = ('', 8888)
server = HTTPServer(address, RequestHandler)
server.serve_forever()
