from .calculate import calculate, CalculationError

class Calculations:

    def __init__(self):
        self.calculations = []

    def add_calculation(self, request):
        request.test_point = '1'
        print(request.path)

    def get_all_calculations(self, request):
        request.test_point = '2'
        print(request.path)

    def get_calculation_by_id(self, request):
        request.test_point = '3'
        print(request.resource_id)
