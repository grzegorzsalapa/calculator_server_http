class EvaluationError(Exception):
    def __init__(self, message: str):
        self.message = message


def evaluate_tokenized_expression(tokenized_expression: list):
    try:
        return _parse_expression(tokenized_expression)
    except ZeroDivisionError as e:
        raise EvaluationError('Invalid expression (division by zero).')
    except Exception as e:
        raise EvaluationError(str(e))



def _parse_expression(tokenized_expression):
    tokens_left = tokenized_expression
    result = _parse_term(tokens_left)
    current_operator = tokens_left[0]

    while current_operator in ['+', '-']:
        tokens_left.pop(0)
        next_term = _parse_term(tokens_left)

        result = _basic_operation(result, next_term, current_operator)
        current_operator = tokens_left[0]

    if current_operator != 'STOP':
        raise EvaluationError('Unexpected error during expression evaluation.')

    return result


def _parse_nested_expression(tokens_left):
    tokens_left.pop(0)
    closing_parenthesis_position = _find_closing_parentesis(tokens_left)

    nested_expression = _extract_nested_expression(tokens_left, closing_parenthesis_position)
    nested_expression.append('STOP')
    nested_expression_result = _parse_expression(nested_expression)

    _remove_tokens_with_nested_expression(tokens_left, closing_parenthesis_position)

    return nested_expression_result


def _basic_operation(x, y, operator):
    if operator == '+':
        return x + y
    elif operator == '-':
        return x - y
    elif operator == '*':
        return x * y
    elif operator == '/':
        return x / y


def _factor_as_number(tokens_left):
    try:
        factor = int(tokens_left[0])
    except ValueError as err:
        err.args = f'Invalid expression ("{tokens_left[0]}" is not an integer).',
        raise
    tokens_left.pop(0)

    return factor


def _find_closing_parentesis(tokens_left):
    try:
        closing_parenthesis_position = tokens_left.index(')')
    except ValueError as err:
        err.args = 'Invalid expression (missing closing parenthesis).',
        raise
    if closing_parenthesis_position == 0:
        raise EvaluationError('Invalid expression (empty parentheses).')

    return closing_parenthesis_position


def _extract_nested_expression(tokens_left, closing_parenthesis_position):
    nested_expression = tokens_left[0:closing_parenthesis_position]

    return nested_expression


def _remove_tokens_with_nested_expression(tokens_left, closing_parenthesis_position):
    del tokens_left[0:closing_parenthesis_position + 1]

    return tokens_left


def _parse_term(tokens_left):
    term_result = _parse_factor(tokens_left)
    current_operator = tokens_left[0]

    while current_operator in ['*', '/']:
        tokens_left.pop(0)
        next_factor = _parse_factor(tokens_left)
        term_result = _basic_operation(term_result, next_factor, current_operator)
        current_operator = tokens_left[0]

    return term_result


def _parse_factor(tokens_left):
    current_token = tokens_left[0]

    if current_token == '(':
        nested_expression_result = _parse_nested_expression(tokens_left)

        return nested_expression_result

    elif current_token == ')':

        raise EvaluationError('Invalid expression (missing opening parenthesis).')
    else:

        return _factor_as_number(tokens_left)
