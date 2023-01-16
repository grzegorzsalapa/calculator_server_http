import pytest
from calculator_server import calculate, CalculationError


def test_calculate_1():
    assert calculate('2+2') == 4


def test_calculate_2():
    assert calculate('5-1') == 4


def test_calculate_3():
    assert calculate(' 2 + 2 -3+6  -4') == 3


def test_calculate_4():
    assert calculate('100 /2') == 50


def test_calculate_5():
    assert calculate('5* 8') == 40


def test_calculate_6():
    assert calculate('81 / 9') == 9


def test_calculate_7():
    assert calculate('2*2+2') == 6


def test_handles_correct_operations_order():
    assert calculate('2 + 2 * 2') == 6


def test_handles_brackets():
    assert calculate('(2+2) * 2') == 8


def test_handles_wrong_argument():
    with pytest.raises(CalculationError, match='Invalid input. Passed argument must be a string.'):
        calculate(2)


def test_handles_forbidden_symbols():
    with pytest.raises(CalculationError, match=r"Invalid expression \(\"2x\" is not an integer\)."):
        calculate('2 + 2x')


def test_handles_division_by_zero():
    with pytest.raises(CalculationError, match="Invalid expression \(division by zero\)."):
        calculate('555 / 0')


def test_handles_opening_with_closing_parentese():
    with pytest.raises(CalculationError, match='Invalid expression \(missing opening parenthesis\).'):
        calculate('3+5+)22*2')


def test_hansles_lack_of_closing_parentesis():
    with pytest.raises(CalculationError, match='Invalid expression \(missing closing parenthesis\).'):
        calculate('25+(3-1')


def test_handles_empty_parentheses():
    with pytest.raises(CalculationError, match='Invalid expression \(empty parentheses\).'):
        assert calculate('2+()')
