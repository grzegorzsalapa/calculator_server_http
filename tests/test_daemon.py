import pytest
from calculator_server.daemon import Resources, Request, _reach_resource_and_execute_request


def test_responds_to_post_expression():
    test_resource = Resources()
    test_request = Request()

    test_request.client_address = ('', '')
    test_request.command = 'POST'
    test_request.path = '/calculations'

    _reach_resource_and_execute_request(test_request, test_resource)
    assert test_request.test_point == '1'


def test_responds_to_get_all_expressions():
    test_resource = Resources()
    test_request = Request()

    test_request.client_address = ('', '')
    test_request.command = 'GET'
    test_request.path = '/calculations'

    _reach_resource_and_execute_request(test_request, test_resource)
    assert test_request.test_point == '2'


def test_responds_to_get_expression_by_id():
    test_resource = Resources()
    test_request = Request()

    test_request.client_address = ('', '')
    test_request.command = 'GET'
    test_request.path = '/calculations/123'

    _reach_resource_and_execute_request(test_request, test_resource)
    assert test_request.test_point == '3'
    assert test_request.resource_id == '123'
