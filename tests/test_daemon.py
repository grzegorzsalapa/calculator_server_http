import pytest
from calculator_server.daemon import Resources, Request, _reach_resource_and_execute_request


def test_responds_to_post_expression():
    test_resource = Resources()
    test_request = Request()

    test_request.client_address = ('', '')
    test_request.command = 'POST'
    test_request.path = '/calculations'
    test_request.json_in = ''
    test_request.expression = '2+2'

    _reach_resource_and_execute_request(test_request, test_resource)
    assert test_request.test_point == '1'


def test_responds_to_get_all_expressions():
    test_resource = Resources()
    test_request = Request()

    test_request.client_address = ('', '')
    test_request.command = 'GET'
    test_request.path = '/calculations'
    test_request.json_in = ''

    _reach_resource_and_execute_request(test_request, test_resource)
    assert test_request.test_point == '2'


def test_responds_to_get_expression_by_id():
    test_resource = Resources()
    test_request = Request()

    def fill_in_resource_with_calculations(arg):
        test_request.client_address = ('127.0.0.1', '')
        test_request.command = 'POST'
        test_request.path = '/calculations'
        test_request.json_in = ''
        test_request.expression = f'{arg} + {arg * 2}'

        _reach_resource_and_execute_request(test_request, test_resource)


    def run_tested_setup():

        test_request.client_address = ('127.0.0.1', '')
        test_request.command = 'GET'
        test_request.path = '/calculations/2'
        test_request.json_in = ''

        _reach_resource_and_execute_request(test_request, test_resource)

    i = 0
    while i < 3:
        fill_in_resource_with_calculations(i)
        i += 1

    run_tested_setup()

    assert test_request.test_point == '3'
    assert test_request.calculation_id == '2'
    assert test_request
