from .calculate import calculate, CalculationError

class Calculations:


    def __init__(self):
        self.calculations = [[], []]


    def add_calculation(self, request):
        request.test_point = '1'
        request.json_out = request.json_in

        expression = request.expression
        try:
            result = str(calculate(expression))
        except CalculationError as e:
            result = str(e)

        client_ip, client_port = request.client_address
        try:
            client_index = self.calculations[0].index(client_ip)
        except ValueError:
            client_index = len(self.calculations[0])
            self.calculations[0].append(client_ip)
            self.calculations[1].append([])

        self.calculations[1][client_index].append((expression, result))

    def get_all_calculations(self, request):
        request.test_point = '2'
        request.json_out = request.json_in

        client_ip, client_port = request.client_address
        client_index = self.calculations[0].index(client_ip)
        print(client_index)

        calculations = self.calculations[1][client_index]
        print(calculations)

    def get_calculation_by_id(self, request):
        request.test_point = '3'
        request.json_out = request.json_in
        print(request.calculation_id)

        client_ip, client_port = request.client_address
        client_index = self.calculations[0].index(client_ip)
        print(client_index)
        calculation_id = int(request.calculation_id) - 1

        calculation = self.calculations[1][client_index][calculation_id]
        print(calculation)
