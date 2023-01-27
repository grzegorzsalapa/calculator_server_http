import pytest
from calculator_server.resources import Resources
from calculator_server.calculations import Calculations

def test_every_request_reaches_the_same_resources_instance():

    resources_for_request_1 = Resources()
    resources_for_request_2 = Resources()

    assert resources_for_request_1.available_resources[1][2] == resources_for_request_2.available_resources[1][2]

def test_paths_map_correct_methods():

    resources_for_request_1 = Resources()
    resources_for_request_2 = Resources()

    assert (resources_for_request_1.available_resources[2][2] == Calculations.get_calculation_by_id and
            resources_for_request_2.available_resources[2][2] == Calculations.get_calculation_by_id)