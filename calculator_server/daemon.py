from http.server import BaseHTTPRequestHandler
import re
from .resources import Resources, ResourceNotFoundError


class CalcDaemon(BaseHTTPRequestHandler):

    def __init__(self, *args, test_setup=False):
        self.resources = Resources()
        if not test_setup:
            super().__init__(*args)

    def do_POST(self):
        self._process_request()

    def do_GET(self):
        self._process_request()

    def _process_request(self):

        try:
            request_in_process = self._collect_request_metadata()
            self._decode_json_from_binary_if_present(request_in_process)

            try:
                _reach_resource_and_execute_request(request_in_process, self.resources)

            except ResourceNotFoundError as e:

                request_in_process.code = 400
                request_in_process.message = str(e)
                request_in_process.json_out = ''

            self._send_response(request_in_process)

        except Exception as e:
            print(f"Unexpected error while handling {self.command} request from client: {self.client_address}")
            print(str(e), '\n')
            raise

    def _collect_request_metadata(self):

        request_metadata = RequestMetadata()
        request_metadata.client_address = self.client_address
        request_metadata.command = self.command
        request_metadata.path = self.path
        return request_metadata

    def _decode_json_from_binary_if_present(self, request):

        try:
            data_length = int(self.headers['Content-Length'])

        except TypeError:
            return

        data_in = self.rfile.read(data_length)
        request.json_in = data_in.decode(encoding='utf-8', errors='strict')

    def _send_response(self, request):

        self.send_response(request.code, request.message)
        self.end_headers()
        b_data = _encode_json_to_binary(request.json_out)
        self.wfile.write(b_data)


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
    else:
        raise ResourceNotFoundError("Resource you are trying to reach does not exist.")


def _encode_json_to_binary(json):

    return bytes(json, 'utf-8')


class RequestMetadata:
    pass
