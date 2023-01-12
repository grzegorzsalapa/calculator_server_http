class ParsingError(Exception):
    def __init__(self, message: str):
        self.message = message


def tokenize_expression(expression_string: str):
    try:
        if type(expression_string) is not str:
            raise TypeError('Invalid input. Passed argument must be a string.')

        operator_tokens = ['+', '-', '*', '/', '(', ')']

        tokenized_expression = []
        term_token = ''
        for char in expression_string:
            if char == " ":
                continue

            if char not in operator_tokens:
                term_token += char

            elif char in operator_tokens:
                if term_token:
                    tokenized_expression.append(term_token)
                    term_token = ''
                tokenized_expression.append(char)
        else:
            if term_token:
                tokenized_expression.append(term_token)
            tokenized_expression.append("STOP")

        return tokenized_expression
    except Exception as e:
        raise ParsingError(str(e))
