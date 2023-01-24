from http.server import BaseHTTPRequestHandler
import re
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
        request_in_process = Request()
        request_in_process.client_address = self.client_address
        request_in_process.command = self.command
        request_in_process.path = self.path

        _reach_resource_and_execute_request(request_in_process, self.resources)
        print(request_in_process.result)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"It's alive!")


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
            request.resource_id = m.group(1)
            return resource[2]


class Request:
    pass


class Resources(Calculations):

    def __init__(self):
        Calculations.__init__(self)

        self.available_resources = [(r'/calculations(\/?$)', 'POST', Calculations.add_calculation),
                                    (r'/calculations(\/?$)', 'GET', Calculations.get_all_calculations),
                                    (r'/calculations/(\d+)', 'GET', Calculations.get_calculation_by_id)]
