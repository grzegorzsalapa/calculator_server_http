import pytest
from calculator_server.daemon import Resources, Request, _reach_resource_and_execute_request


def test_reaches_post_expression():
    test_resource = Resources()
    test_request = Request()

    test_request.client_address = ('', '')
    test_request.command = 'POST'
    test_request.path = '/calculations'
    test_request.json_in = ''
    test_request.expression = '2+2'

    _reach_resource_and_execute_request(test_request, test_resource)
    assert test_request.test_point == '1'


def test_reaches_get_all_expressions():
    test_resource = Resources()
    test_request = Request()

    test_request.client_address = ('', '')
    test_request.command = 'GET'
    test_request.path = '/calculations'
    test_request.json_in = ''

    _reach_resource_and_execute_request(test_request, test_resource)
    assert test_request.test_point == '2'


def test_reaches_get_expression_by_id():
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


def test_responds_with_correct_json_to_get_expression_by_id():
    test_resource = Resources()
    test_request = Request()

    def fill_in_resource_with_calculations(arg):
        test_request.client_address = ('127.0.0.2', '')
        test_request.command = 'POST'
        test_request.path = '/calculations'
        test_request.json_in = ''
        test_request.expression = f'{arg} + {arg * 2}'

        _reach_resource_and_execute_request(test_request, test_resource)

    def run_tested_setup():

        test_request.client_address = ('127.0.0.2', '')
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
    assert test_request.json_out == '[{"id":"2", "expression":"1 + 2", "result":"3"},]'


def test_responds_with_correct_json_to_get_all_expressions():
    test_resource = Resources()
    test_request = Request()

    def fill_in_resource_with_calculations(arg):
        test_request.client_address = ('127.0.0.3', '')
        test_request.command = 'POST'
        test_request.path = '/calculations'
        test_request.json_in = ''
        test_request.expression = f'{arg} + {arg * 2}'

        _reach_resource_and_execute_request(test_request, test_resource)

    def run_tested_setup():

        test_request.client_address = ('127.0.0.3', '')
        test_request.command = 'GET'
        test_request.path = '/calculations'
        test_request.json_in = ''

        _reach_resource_and_execute_request(test_request, test_resource)

    i = 0
    while i < 3:
        fill_in_resource_with_calculations(i)
        i += 1

    run_tested_setup()

    assert test_request.test_point == '2'
    assert test_request.json_out == '[{"id":"1", "expression":"0 + 0", "result":"0"},' \
                                    '{"id":"2", "expression":"1 + 2", "result":"3"},' \
                                    '{"id":"3", "expression":"2 + 4", "result":"6"},]'


def test_all_request_reach_the_same_resources():
    test_resource = Resources()
    test_request = Request()

    def fill_in_resource_with_calculations(arg: int, addr: int):
        test_request.client_address = (f'127.0.0.{addr}', '')
        test_request.command = 'POST'
        test_request.path = '/calculations'
        test_request.json_in = ''
        test_request.expression = f'{arg} + {arg * 2}'

        print(test_request.client_address)
        _reach_resource_and_execute_request(test_request, test_resource)

    def run_tested_setup():

        test_request.client_address = ('127.0.0.6', '')
        test_request.command = 'GET'
        test_request.path = '/calculations/2'
        test_request.json_in = ''

        _reach_resource_and_execute_request(test_request, test_resource)

    i = 0
    c = 5

    while c < 8:
        while i < 3:
            fill_in_resource_with_calculations(i + c, c)
            i += 1
        c += 1
        i = 0

    run_tested_setup()

    assert test_request.test_point == '3'
    assert test_request.calculation_id == '2'
    assert test_request.json_out == '[{"id":"2", "expression":"7 + 14", "result":"21"},]'
