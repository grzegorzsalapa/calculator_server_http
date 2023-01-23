from http.server import BaseHTTPRequestHandler
from .calculate import calculate, CalculationError


class CalcDaemon(BaseHTTPRequestHandler):

    def which_endpoint_POST(self):
        path = self.path
        if path == '/calculations':
            pass
        else:
            pass  # some "forbidden call" response

    def which_endpoint_GET(self):
        path = self.path
        if path == '/calculations':
            print(path)
        elif path[0:13] == '/calculations/':
            print(path)
        else:
            pass  # some "forbidden call" response

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'POST is alive!')

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'GET is alive!')
        pass
