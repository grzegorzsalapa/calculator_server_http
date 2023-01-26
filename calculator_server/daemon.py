from http.server import BaseHTTPRequestHandler
import re
from .resources import Resources, ResourceNotFoundError


class CalcDaemon(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.resources = Resources()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        self._process_request()

    def do_GET(self):
        self._process_request()

    def _process_request(self):

        request_in_process = self._collect_request_metadata()
        request_in_process.json_in = self._decode_json()

        try:
            _reach_resource_and_execute_request(request_in_process, self.resources)

        except ResourceNotFoundError as e:

            request_in_process.code = 400
            request_in_process.message = str(e)
            request_in_process.json_out = ''

        self._send_response(request_in_process)

    def _collect_request_metadata(self):

        request_metadata = RequestMetadata()
        request_metadata.client_address = self.client_address
        request_metadata.command = self.command
        request_metadata.path = self.path
        return request_metadata

    def _decode_json(self):

        data_length = int(self.headers['Content-Length'])
        data_in = self.rfile.read(data_length)

        return data_in.decode(encoding='utf-8', errors='strict')

    def _send_response(self, request):

        self.send_response(request.code, request.message)
        self.end_headers()
        b_data = _encode_json(request.json_out)
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


def _encode_json(json):

    return bytes(json, 'utf-8')


class RequestMetadata:
    pass
