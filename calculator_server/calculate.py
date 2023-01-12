from calculator_server.evaluator import evaluate_tokenized_expression, EvaluationError
from calculator_server.parser import tokenize_expression, ParsingError


class CalculationError(Exception):
    def __init__(self, message: str):
        self.message = message


def calculate(expression: str):
    try:
        tokenized_expression = tokenize_expression(expression)

        return evaluate_tokenized_expression(tokenized_expression)

    except ParsingError as err:

        raise CalculationError(str(err))

    except EvaluationError as err:

        raise CalculationError(str(err))
