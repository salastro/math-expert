"""Testing MathDocument methods"""
import pytest

from mathexpert.func import MathDocument

doc = MathDocument()


@pytest.mark.parametrize("test_input, expected", [
    ("(sin(x) ** 2 - cos(x) ** 2) / (cos(x) ** 2 * sin(x) ** 2)",
        "((sin(x)**2 - cos(x)**2)/(sin(x)**2*cos(x)**2), 2/sin(2*x))"),
    ("x^x", "(x**x, 'No Computable Integral')"),
    ("exp(-x^2)", "(exp(-x**2), sqrt(pi)*erf(x)/2)"),
])
def test_inte(test_input, expected):
    """Testing integration.

    :param test_input: equation
    :param expected: result
    """
    assert str(doc.inte(test_input)) == expected


@pytest.mark.parametrize("test_input, expected", [
    ("x**(1/x)", "(x**(1/x), 1, x**(-2 + 1/x)*(1 - log(x)))"),
    ("x**(1/x), 2",
        "(x**(1/x), 2, x**(-4 + 1/x)*(x*(2*log(x) - 3) + (log(x) - 1)**2))"),
])
def test_diff(test_input, expected):
    """Testing differentiation.

    :param test_input: equation
    :param expected: result
    """
    assert str(doc.diff(test_input)) == expected


@pytest.mark.parametrize("test_input, expected", [
    ("2/sin(2*x),oo", "(2/sin(2*x), oo, '+', 'No Computable Limit')"),
    ("(sin(x)^2 - cos(x)^2) / (cos(x)^2 * sin(x)^2), oo",
        "((sin(x)**2 - cos(x)**2)/(sin(x)**2*cos(x)**2), oo, '+', 'No Computable Limit')"),
    ("(x^3-4*x)/(2*x^2+3*x)", "('(x^3-4*x)/(2*x^2+3*x)', 0, '+', -4/3)"),
    ("sin(x), oo", "(sin(x), oo, '+', AccumBounds(-1, 1))"),
])
def test_lim(test_input, expected):
    """Testing limits.

    :param test_input: equation
    :param expected: result
    """
    assert str(doc.lim(test_input)) == expected


@pytest.mark.parametrize("test_input, expected", [
    ("x+3=1", "([x + 3, 1], [-2])"),
    ("x+3>1", "(x + 3 > 1, (-2 < x) & (x < oo))"),
    ])
def test_sol(test_input, expected):
    """Testing solving.

    :param test_input: equation
    :param expected: result
    """
    assert str(doc.sol(test_input)) == expected


@pytest.mark.parametrize("test_input, expected", [
    ("2^2", "(2**2, 4)"),
    ("sqrt(2)", "(sqrt(2), 1.41421356237310)"),
    ("sin(2)", "(sin(2), 0.909297426825682)"),
    ("sin(45/cos(3))", "(sin(45/cos(3)), -0.995181909173319)"),
    ("sin(1j)", "(sin(1*I), 1.1752011936438*I)"),
    ])
def test_eval(test_input, expected):
    """Testing evaluation.

    :param test_input: equation
    :param expected: result
    """
    assert str(doc.eval(test_input)) == expected
