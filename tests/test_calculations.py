import pytest
from calculator_server.calculations import Calculations
from calculator_server.daemon import RequestMetadata


def test_expression_from_valid_json_is_added_to_calculations_record():

    def test_prep():
        request = RequestMetadata()
        request.client_address = ('127.0.0.1', '23452')
        request.json_in = '{"expression":"2+2"}'
        calculations = Calculations()

        return request, calculations

    request, calculations = test_prep()
    calculations.add_calculation(request)

    assert request.json_out == "{/calculations/1}"


def test_returns_all_calculations_of_given_client():
    def test_prep():
        request = RequestMetadata()
        request.client_address = ('127.0.0.1', '23452')
        request.json_in = '{"expression":"2+2"}'
        calculations = Calculations()
        calculations.add_calculation(request)

        request.json_in = '{"expression":"2/0"}'
        calculations.add_calculation(request)

        request.json_in = '{"expression":"(26-8) / 9"}'
        calculations.add_calculation(request)

        request.json_in = ''

        return request, calculations


    request, calculations = test_prep()
    calculations.get_all_calculations(request)

    assert request.json_out == '[{"id":"1", "expression":"2+2", "result":"4"},' \
                               '{"id":"2", "expression":"2/0", "result":"Invalid expression (division by zero)."},' \
                               '{"id":"3", "expression":"(26-8) / 9", "result":"2.0"},]'


def test_returns_all_calculations_of_given_client():
    def test_prep(id):
        request = RequestMetadata()
        request.client_address = ('127.0.0.1', '23452')
        request.json_in = '{"expression":"2+2"}'
        calculations = Calculations()
        calculations.add_calculation(request)

        request.json_in = '{"expression":"2/0"}'
        calculations.add_calculation(request)

        request.json_in = '{"expression":"(26-8) / 9"}'
        calculations.add_calculation(request)

        request.calculation_id = id

        return request, calculations


    request, calculations = test_prep('2')
    calculations.get_calculation_by_id(request)

    assert request.json_out == '[{"id":"2", "expression":"2/0", "result":"Invalid expression (division by zero)."},]'
