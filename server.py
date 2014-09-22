import cgi
import re
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer

gets = {}
posts = {}


def __register_url(url_dict, url, func):
    url_pattern = ''
    params = []
    url_list = url.split('/')
    url_list.pop(0)
    for u in url_list:
        if u.find(':') == 0:
            params.append(u.replace(':', ''))
            u = '(\w+)'
        url_pattern += '/' + u
    url_dict[url_pattern] = func


def get(url):
    def _(f):
        __register_url(gets, url, f)
    return _


def post(url):
    def _(f):
        __register_url(posts, url, f)
    return _


class RequestHandler(BaseHTTPRequestHandler):

    def __get_path(self):
        return urlparse.urlparse(self.path).path

    def __process_url_dict(self, url_dict, data):
        path = self.__get_path()
        for url, func in url_dict.iteritems():
            m = re.match(url, path)
            if bool(m):
                message = func(self, data, *m.groups())
                self.send_response(200)
                self.end_headers()
                self.wfile.write(message)
                return
        self.send_response(404)
        self.end_headers()
        self.wfile.write('404 Not Found')

    def __get_query(self):
        parsed_path = urlparse.urlparse(self.path)
        return urlparse.parse_qs(parsed_path.query)

    def do_GET(self):
        self.__process_url_dict(gets, self.__get_query())

    def do_POST(self):
        content_type, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if content_type == 'multipart/form-data':
            data = cgi.parse_multipart(self.rfile, pdict)
        elif content_type == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            data = urlparse.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            self.send_response(415)
            self.end_headers()
            self.wfile.write('415 Unsupported Media Type')
            return
        self.__process_url_dict(posts, data)

def run(host = '', port = 8888):
    address = (host, port)
    server = HTTPServer(address, RequestHandler)
    server.serve_forever()

