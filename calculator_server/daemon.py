from http.server import BaseHTTPRequestHandler
import re
from .calculate import calculate, CalculationError


class CalcDaemon(BaseHTTPRequestHandler):

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'POST is alive!')

    def do_GET(self):
        _parse_path_to_resource(self.path)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'GET is alive!')


def _parse_path_to_resource(path: str):
    pattern = re.compile(r'/calculations/(\d+)')
    m = pattern.match(path)
    if m:
        print(m.group(1))

class AvailableResources():

    def __init__(self):
        self.list = [(r'/calculations/(\d+)', ]


class Calculations(self):

    def __init__(self):
        self.calculations = []

    def add_calculation(self):
        pass

    def get_all_calculations(self):
        pass

    def get_calculation_by_id(self):
        pass
