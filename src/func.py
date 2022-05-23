from __future__ import division

import logging

from pylatex import Alignat, Axis, Center, Command, Document, Plot, TikZ
# Section, Subsection, Math, Figure, Matrix,
from pylatex.utils import NoEscape
from sympy import (Derivative, Eq, Integral, Limit, diff, factor, integrate,
                   limit, simplify, solve, sympify, trigsimp)
# from sympy.integrals.manualintegrate import manualintegrate, integral_steps
# from sympy.integrals.risch import NonElementaryIntegral
from sympy.abc import x
from sympy.printing import latex


class MathDoc(Document):
    def __init__(self):
        super().__init__()
        # TODO: add preamble change gemotry

    def doc_heading(self, title: str, author: str, date: str = r"\today") -> None:
        self.preamble.append(Command("title", title))
        self.preamble.append(Command("author", author))
        self.preamble.append(Command("date", NoEscape(date)))
        logging.debug(f"Title: {title}")
        logging.debug(f"Author: {author}")
        logging.debug(f"Date: {date}")
        self.append(NoEscape(r"\maketitle"))

    def doc_append(self, *equations: str) -> None:
        """Append a sequence of experssions into the document

        :*equations: the experssions to be added to the document
        :returns: None

        """
        with self.create(Alignat(numbering=True, escape=False)) as agn:
            for equation in equations:
                if equation is not None:
                    agn.append(equation)
                logging.debug(f"Appended: {equation}")

    def inte(self, equation: str) -> None:
        logging.debug(f"Orignial Equation: {equation}")
        solvable = True
        equation = sympify(equation)
        logging.debug(f"Sympifyed Equation: {equation}")
        solution = trigsimp(simplify(integrate(equation, x)))
        # solution = integrate(trigsimp(simplify(equation)), x)
        equation = Integral(equation, x)
        if str(equation) == str(solution):
            solution = "No Computable Integral"
            solvable = False
        logging.debug(f"Solution: {solution}")
        self.doc_append(
            latex(equation),
            r"=",
            latex(solution),
            r"+C" if solvable else None
        )

    def diff(self, equation: str) -> None:
        logging.debug(f"Orignial Equation: {equation}")
        eq_fmt = equation.split(",")
        equation = sympify(eq_fmt[0])
        logging.debug(f"Sympifyed Equation: {equation}")
        order = int(eq_fmt[1]) if len(eq_fmt) == 2 else 1
        logging.debug(f"Derivative order: {order}")
        solution = simplify(diff(equation, x, order))
        equation = Derivative(equation, x, order)
        logging.debug(f"Solution: {solution}")
        self.doc_append(latex(equation), r"=", latex(solution))

    def lim(self, equation: str) -> None:
        logging.debug(f"Orignial Equation: {equation}")
        eq_fmt = list(map(sympify, equation.split(",")))
        match len(eq_fmt):
            case 1:
                show, approach, sign = equation, 0, "+"
            case 2:
                show, approach, sign = eq_fmt[0], eq_fmt[1], "+"
            case 3:
                show, approach, sign = eq_fmt[0], eq_fmt[1], eq_fmt[2]
        solution = limit(show, x, approach, sign)
        logging.debug(f"Sympifyed Equation: {show}")
        logging.debug(f"Approach to: {approach}")
        logging.debug(f"Sign: {sign}")
        if Limit(show, x, approach, sign) == solution:
            solution = "No Computable Limit"
        logging.debug(f"Solution: {solution}")
        self.doc_append(latex(Limit(show, x, approach, sign)), r"=", latex(solution))

    def simp(self, equation: str) -> None:
        logging.debug(f"Orignial Equation: {equation}")
        equation = sympify(equation)
        logging.debug(f"Sympifyed Equation: {equation}")
        solution = trigsimp(simplify(equation))
        logging.debug(f"Solution: {solution}")
        self.doc_append(latex(equation), r"=", latex(solution))

    def fact(self, equation: str) -> None:
        logging.debug(f"Orignial Equation: {equation}")
        equation = sympify(equation)
        logging.debug(f"Sympifyed Equation: {equation}")
        solution = factor(equation)
        solution = trigsimp(simplify(equation))
        logging.debug(f"Solution: {solution}")
        self.doc_append(latex(equation), r"=", latex(solution))

    def sol(self, equation: str) -> None:
        logging.debug(f"Orignial Equation: {equation}")
        if "=" in equation:
            eq_fmt = list(map(sympify, equation.split("=")))
            logging.debug(f"Sympifyed Equation: {eq_fmt[0]} = {eq_fmt[1]}")
            solution = solve(Eq(eq_fmt[0], eq_fmt[1]))
            is_x = True
        else:
            equation = sympify(equation)
            logging.debug(f"Sympifyed Equation: {equation}")
            solution = solve(sympify(equation))
            is_x = False
        logging.debug(f"Solution: {solution}")
        self.doc_append(
            latex(equation)
            if not is_x
            else rf"{latex(sympify(eq_fmt[0]))} = {latex(sympify(eq_fmt[1]))}",
            r"\Rightarrow",
            r"x=",
            latex(solution),
        )

    def eval(self, equation: str) -> None:
        from numpy import (arccos, arcsin, arctan, cos, exp, log, log10, pi,
                           sin, sqrt, tan)

        logging.debug(f"Orignial Equation: {equation}")
        solution = sympify(eval(equation.replace("^", "**")))
        equation = sympify(equation, evaluate=False)
        logging.debug(f"Sympifyed Equation: {equation}")
        logging.debug(f"Solution: {solution}")
        # solution = eval(equation)
        self.doc_append(latex(equation), r"=", latex(solution))

    def plot(
        self,
        equation: str,
        height: str = "6cm",
        width: str = "6cm",
        grid: str = "both",
        axis_lines: str = "middle",
    ) -> None:
        logging.debug(f"Orignial Equation: {equation}")
        logging.debug(f"Gemotry: {height}, {width}")
        logging.debug(f"Grid: {grid}")
        logging.debug(f"Axis: {axis_lines}")
        with self.create(Center()):
            with self.create(TikZ()):
                plot_options = f"height={height}, width={width}, grid={grid}, axis lines={axis_lines}"
                with self.create(Axis(options=plot_options)) as plot:
                    plot.append(Plot(name=equation, func=equation))


if __name__ == "__main__":
    LEVEL = logging.DEBUG
    FMT = '[%(levelname)s] %(asctime)s - %(funcName)s|%(message)s'
    logging.basicConfig(level=LEVEL, format=FMT)

    # geometry_options = {"tmargin": "1cm", "lmargin": "10cm"}
    doc = MathDoc()
    FILE = "full"

    doc.doc_heading(title="Func.Py Tests", author="SalahDin Rezk")

    doc.inte("(sin(x) ** 2 - cos(x) ** 2) / (cos(x) ** 2 * sin(x) ** 2)")
    doc.inte("x^x")
    doc.inte("exp(-x^2)")
    doc.diff("x**(1/x)")
    doc.diff("x**(1/x), 2")
    doc.lim("2/sin(2*x),oo")
    doc.lim("(sin(x)^2 - cos(x)^2) / (cos(x)^2 * sin(x)^2), oo")
    doc.lim("(x^3-4*x)/(2*x^2+3*x)")
    doc.lim("sin(x), oo")
    doc.sol("x+3=1")
    doc.sol("x+3>1")
    doc.eval("2^2")
    doc.eval("sqrt(2)")
    doc.eval("sin(2)")
    doc.eval("sin(45/cos(3))")
    doc.eval("sin(1j)")

    doc.generate_pdf(FILE, clean_tex=True)
