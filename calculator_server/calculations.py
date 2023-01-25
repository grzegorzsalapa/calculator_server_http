from .calculate import calculate, CalculationError
import re


class Calculations:

    def __init__(self):
        self.calculations = [[], []]

    def add_calculation(self, request):
        request.test_point = '1'

        expression = _unpack_json(request.json_in)

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

        calculation_id = len(self.calculations[1][client_index]) + 1
        self.calculations[1][client_index].append((calculation_id, expression, result))
        request.json_out = 'Done'

    def get_all_calculations(self, request):
        request.test_point = '2'

        client_ip, client_port = request.client_address
        client_index = self.calculations[0].index(client_ip)
        print(client_index)

        calculations = self.calculations[1][client_index]
        request.calculations = calculations

        request.json_out = _pack_in_json(calculations)

    def get_calculation_by_id(self, request):
        request.test_point = '3'

        client_ip, client_port = request.client_address
        client_index = self.calculations[0].index(client_ip)
        print(client_index)
        calculation_id = int(request.calculation_id) - 1

        calculations = [self.calculations[1][client_index][calculation_id]]
        request.calculations = calculations

        request.json_out = _pack_in_json(calculations)


def _pack_in_json(calculations):
    json = '['
    i = 1
    for tup in calculations:
        json = json + '{' + f'"id":"{tup[0]}", "expression":"{tup[1]}", "result":"{tup[2]}"' + '},'
        i += 1
    json += ']'

    return json


def _unpack_json(json_in):
    json = json_in
    pattern = re.compile(r'\{"expression":"(.*?)"}')
    m = pattern.match(json)
    expression = m.group(1)

    return expression
