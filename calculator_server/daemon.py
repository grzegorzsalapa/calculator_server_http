from http.server import BaseHTTPRequestHandler
import re
import io
from .calculations import Calculations


class CalcDaemon(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.resources = Resources()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        self._process_request()

    def do_GET(self):
        self._process_request()

    def _process_request(self):
        # data_in = bytearray()
        # b_no = self.rfile.readinto(data_in)
        #
        # print(data_in, b_no, self.path, self.command)
        # json_in = data_in.decode(encoding='utf-8', errors='strict')
        json_in = '{ "expression":"2+2"}'
        expression = "2+2"

        request_in_process = Request()
        request_in_process.client_address = self.client_address
        request_in_process.command = self.command
        request_in_process.path = self.path
        request_in_process.json_in = json_in
        request_in_process.expression = expression

        _reach_resource_and_execute_request(request_in_process, self.resources)

        data_out = bytes(request_in_process.json_out, 'utf-8')

        self.send_response(200)
        self.end_headers()
        self.wfile.write(data_out)


def _reach_resource_and_execute_request(request, resources):
    method_to_execute_on_resource = _parse_path_and_command(request, resources)
    method_to_execute_on_resource(resources, request)


def _parse_path_and_command(request, resources):
    path = request.path
    command = request.command
    resource_list = resources.available_resources
    for resource in resource_list:
        pattern = re.compile(resource[0])
        m = pattern.match(path)
        if m and command == resource[1]:
            request.calculation_id = m.group(1)
            return resource[2]


class Request:
    pass


class SingletonMeta(type):  # TODO: Ripped off. Need to understand what's going on...

    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Resources(Calculations, metaclass=SingletonMeta):

    def __init__(self):
        Calculations.__init__(self)

        self.available_resources = [(r'/calculations(\/?$)', 'POST', Calculations.add_calculation),
                                    (r'/calculations(\/?$)', 'GET', Calculations.get_all_calculations),
                                    (r'/calculations/(\d+)', 'GET', Calculations.get_calculation_by_id)]
