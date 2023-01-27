import pytest
from unittest.mock import MagicMock
from calculator_server.daemon import CalcDaemon, RequestMetadata, _parse_path_and_command, ResourceNotFoundError
from calculator_server.resources import Resources
from calculator_server.calculations import Calculations


def _set_up_mocked_request_handler(ip_address: str, path: str, command: str, json: str):
    request_handler_mock = CalcDaemon(test_setup=True)
    request_handler_mock.client_address = (f'{ip_address}', '5')
    request_handler_mock.command = command
    request_handler_mock.path = path
    request_handler_mock.headers = MagicMock()
    request_handler_mock.rfile = MagicMock()
    request_handler_mock.rfile.read = MagicMock(return_value=bytes(json, 'utf-8'))
    request_handler_mock.send_response = MagicMock()
    request_handler_mock.end_headers = MagicMock()
    request_handler_mock.wfile = MagicMock()
    request_handler_mock.wfile.write = MagicMock()

    return request_handler_mock


def test_creates_resource_with_passed_expression():

    request_handler_mock = _set_up_mocked_request_handler('127.0.0.1', '/calculations', 'POST', '{"expression":"2+2"}')
    request_handler_mock.do_POST()

    request_handler_mock.send_response.assert_called_once_with(201, "Calculation added to record with id:1.")
    request_handler_mock.wfile.write.assert_called_once_with(b'{"url":"/calculations/1"}')

def test_responds_with_correct_json_to_get_expression_by_id():

    def fill_in_resource_with_calculations():

        for i in range(10):
            request_handler_mock = _set_up_mocked_request_handler('127.0.0.2', '/calculations', 'POST',
                                                                  '{' + f'"expression":"{i} + {i * 2}"' + '}')
            request_handler_mock.do_POST()

    fill_in_resource_with_calculations()
    request_handler_mock = _set_up_mocked_request_handler('127.0.0.2', '/calculations/6', 'GET', '')
    request_handler_mock.do_POST()

    request_handler_mock.send_response.assert_called_once_with(302, "Returned requested calculation.")
    request_handler_mock.wfile.write.assert_called_once_with(b'[{"id":"6", "expression":"5 + 10", "result":"15"},]')


def test_responds_with_correct_json_to_get_all_expressions():

    def fill_in_resource_with_calculations():

        for i in range(3):
            request_handler_mock = _set_up_mocked_request_handler('127.0.0.3', '/calculations', 'POST',
                                                                  '{' + f'"expression":"{i} + {i * 2}"' + '}')
            request_handler_mock.do_POST()

    fill_in_resource_with_calculations()
    request_handler_mock = _set_up_mocked_request_handler('127.0.0.3', '/calculations', 'GET', '')
    request_handler_mock.do_POST()

    request_handler_mock.send_response.assert_called_once_with(302, "Returned requested calculations.")
    request_handler_mock.wfile.write.assert_called_once_with(b'[{"id":"1", "expression":"0 + 0", "result":"0"},'
                                                             b'{"id":"2", "expression":"1 + 2", "result":"3"},'
                                                             b'{"id":"3", "expression":"2 + 4", "result":"6"},]')


def test_handles_get_request_for_not_existing_resource_id():

    def fill_in_resource_with_calculations():

        for i in range(10):
            request_handler_mock = _set_up_mocked_request_handler('127.0.0.5', '/calculations', 'POST',
                                                                  '{' + f'"expression":"{i} + {i * 2}"' + '}')
            request_handler_mock.do_POST()

    fill_in_resource_with_calculations()
    request_handler_mock = _set_up_mocked_request_handler('127.0.0.5', '/calculations/15', 'GET', '')
    request_handler_mock.do_POST()

    request_handler_mock.send_response.assert_called_once_with(204, "Record with id: 15 does not exist.")
    request_handler_mock.wfile.write.assert_called_once_with(b'')


def test_handles_get_request_for_all_resources_by_client_with_no_record():

    request_handler_mock = _set_up_mocked_request_handler('127.0.0.7', '/calculations', 'GET', '')
    request_handler_mock.do_POST()

    request_handler_mock.send_response.assert_called_once_with(302, "No records were found.")
    request_handler_mock.wfile.write.assert_called_once_with(b'')


def test_all_request_reach_the_same_resources():

    def fill_in_resource_with_calculations():

        for j in range (10, 20):
            for i in range(3):
                request_handler_mock = _set_up_mocked_request_handler(f'127.0.0.{j}', '/calculations', 'POST',
                                                                      '{' + f'"expression":"{i * j} + {i * j * 2}"' + '}')
                request_handler_mock.do_POST()

    fill_in_resource_with_calculations()
    request_handler_mock = _set_up_mocked_request_handler('127.0.0.16', '/calculations/2', 'GET', '')
    request_handler_mock.do_POST()

    request_handler_mock.send_response.assert_called_once_with(302, "Returned requested calculation.")
    request_handler_mock.wfile.write.assert_called_once_with(b'[{"id":"2", "expression":"16 + 32", "result":"48"},]')


def test_handles_missing_jason():

    request_handler_mock = _set_up_mocked_request_handler('127.0.0.1', '/calculations', 'POST', '')
    request_handler_mock.do_POST()

    request_handler_mock.send_response.assert_called_once_with(400, "Request missing json file.")
    request_handler_mock.wfile.write.assert_called_once_with(b'')


def test_handles_invalid_jason():

    request_handler_mock = _set_up_mocked_request_handler('127.0.0.1', '/calculations', 'POST', '{"nonsense"+"4/0"}')
    request_handler_mock.do_POST()

    request_handler_mock.send_response.assert_called_once_with(400, "Invalid format of JSON file.")
    request_handler_mock.wfile.write.assert_called_once_with(b'')


def test_handles_request_on_invalid_endpoints():

    request_handler_mock = _set_up_mocked_request_handler('127.0.0.1', '/calculat', 'POST', '{""expression":"2+2""}')
    request_handler_mock.do_POST()

    request_handler_mock.send_response.assert_called_once_with(400, "Resource you are trying to reach does not exist.")
    request_handler_mock.wfile.write.assert_called_once_with(b'')

    request_handler_mock = _set_up_mocked_request_handler('127.0.0.1', '/calculations/foo', 'GET', '')
    request_handler_mock.do_POST()

    request_handler_mock.send_response.assert_called_once_with(400, "Resource you are trying to reach does not exist.")
    request_handler_mock.wfile.write.assert_called_once_with(b'')


def test_parsing_of_request_path_and_command_post_calculation():

    def test_prep():
        resources = Resources()
        request = RequestMetadata()
        request.path = "/calculations"
        request.command = "POST"

        return request, resources

    request, resources = test_prep()
    result_method = _parse_path_and_command(request, resources)

    assert result_method == Calculations.add_calculation

def test_parsing_of_request_path_and_command_get_calculation_by_id():

    def test_prep():
        resources = Resources()
        request = RequestMetadata()
        request.path = "/calculations/3"
        request.command = "GET"

        return request, resources

    request, resources = test_prep()
    result_method = _parse_path_and_command(request, resources)

    assert result_method == Calculations.get_calculation_by_id


def test_parsing_of_request_path_and_command_get_all_calculations():

    def test_prep():
        resources = Resources()
        request = RequestMetadata()
        request.path = "/calculations"
        request.command = "GET"

        return request, resources

    request, resources = test_prep()
    result_method = _parse_path_and_command(request, resources)

    assert result_method == Calculations.get_all_calculations


def test_handles_invalid_path_and_command():

    def test_prep():
        resources = Resources()
        request = RequestMetadata()
        request.path = "/calculations/15"
        request.command = "POST"

        return request, resources

    request, resources = test_prep()

    with pytest.raises(ResourceNotFoundError, match='Resource you are trying to reach does not exist.'):
        _parse_path_and_command(request, resources)