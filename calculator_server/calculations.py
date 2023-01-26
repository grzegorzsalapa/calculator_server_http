from .calculate import calculate, CalculationError
import re


class Calculations:

    def __init__(self):
        self.calculations = [[], []]

    def add_calculation(self, request):

        request.test_point = '1'

        if request.json_in == '':

            request.code = 400
            request.message = "Request missing json file."
            request.json_out = ''

            return

        try:
            expression = _unpack_json(request.json_in)

        except AttributeError:

            request.code = 400
            request.message = "Invalid format of JSON file."
            request.json_out = ''

            return

        result = _get_calc_result(expression)

        client_index = self._find_client_or_create_new(request)
        calculation_id = self._add_calculation_to_clients_record_and_set_id(client_index, expression, result)

        request.code = 201
        request.message = f"Calculation added to record with id:{calculation_id}."
        request.json_out = ''

    def get_all_calculations(self, request):

        request.test_point = '2'

        client_ip, client_port = request.client_address
        try:
            client_index = self.calculations[0].index(client_ip)

        except ValueError:

            request.code = 302
            request.message = "No records were found."
            request.json_out = ''

            return

        calculations = self.calculations[1][client_index]

        request.code = 302
        request.message = "Returned requested calculations."
        request.json_out = _pack_in_json(calculations)

    def get_calculation_by_id(self, request):

        request.test_point = '3'

        client_ip, client_port = request.client_address
        try:
            client_index = self.calculations[0].index(client_ip)

        except ValueError:

            request.code = 204
            request.message = "No records were found."
            request.json_out = ''

            return

        calculation_id = int(request.calculation_id) - 1
        try:
            calculations = [self.calculations[1][client_index][calculation_id]]

        except IndexError:

            request.code = 204
            request.message = f"Record with id: {request.calculation_id} does not exist."
            request.json_out = ''

            return

        request.code = 302
        request.message = "Returned requested calculation."
        request.json_out = _pack_in_json(calculations)

    def _find_client_or_create_new(self, request):

        client_ip, client_port = request.client_address
        try:
            client_index = self.calculations[0].index(client_ip)
        except ValueError:
            client_index = len(self.calculations[0])
            self.calculations[0].append(client_ip)
            self.calculations[1].append([])

        return client_index

    def _add_calculation_to_clients_record_and_set_id(self, client_index, expression, result):

        calculation_id = len(self.calculations[1][client_index]) + 1
        self.calculations[1][client_index].append((calculation_id, expression, result))

        return calculation_id


def _get_calc_result(expression):

    try:
        result = str(calculate(expression))
    except CalculationError as e:
        result = str(e)

    return result


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
