from .calculate import calculate, CalculationError
import re
import json
from json import JSONDecodeError


class Calculations:

    def __init__(self):
        self.calculations = [[], []]

    def add_calculation(self, request):

        if request.json_in == '':

            request.code = 400
            request.message = "Request missing json file."
            request.json_out = ''

            return

        try:
            expression = _unpack_json(request.json_in)

        except (JSONDecodeError, KeyError) as e:

            request.code = 400
            request.message = "Invalid format of JSON file."
            request.json_out = ''

            return

        result = _get_calc_result(expression)

        client_index = self._find_client_or_create_new(request)
        calculation_id = self._add_calculation_to_clients_record_and_set_id(client_index, expression, result)

        request.code = 201
        request.message = f"Calculation added to record with id:{calculation_id}."
        request.json_out = _pack_in_json({"url": f'/calculations/{calculation_id}'})

    def get_all_calculations(self, request):

        client_ip, client_port = request.client_address
        try:
            client_index = self.calculations[0].index(client_ip)

        except ValueError:

            request.code = 302
            request.message = "No records were found."
            request.json_out = ''

            return

        calculations = self.calculations[1][client_index]
        payload = _pack_calculations(calculations)

        request.code = 302
        request.message = "Returned requested calculations."
        request.json_out = _pack_in_json(payload)

    def get_calculation_by_id(self, request):

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

        payload = _pack_calculations(calculations)

        request.code = 302
        request.message = "Returned requested calculation."
        request.json_out = _pack_in_json(payload)

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


def _pack_calculations(calculations):

    payload = []
    i = 1
    for tup in calculations:
        payload.append({'id': f'{tup[0]}', 'expression': f'{tup[1]}', 'result': f'{tup[2]}'})
        i += 1

    return payload

def _pack_in_json(payload):

    json_ = json.dumps(payload)

    return json_


def _unpack_json(json_in):

    json_ = json_in
    dict = json.loads(json_)
    expression = dict['expression']

    return expression
