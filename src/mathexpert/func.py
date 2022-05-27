"""Functions that operates on the math document."""
from __future__ import division

from functools import reduce
from operator import mul

from loguru import logger
from numpy import (arccos, arcsin, arctan, cos, exp, log, log10, matrix, pi,
                   sin, sqrt, tan)
from pylatex import (Alignat, Axis, Center, Command, Document, Matrix, Plot,
                     TikZ)
# Matrix  Section, Subsection, Math, Figure
from pylatex.utils import NoEscape
from sympy import (Derivative, Eq, Integral, Limit, diff, factor, integrate,
                   limit, simplify, solve, sympify, trigsimp)
# from sympy.integrals.manualintegrate import manualintegrate, integral_steps
# from sympy.integrals.risch import NonElementaryIntegral
from sympy.abc import x
from sympy.printing import latex


class MathDocument(Document):
    """MathDocument."""

    def __init__(self):
        """__init__."""
        super().__init__()
        # TODO: add preamble change gemotry

    def doc_heading(
            self, title: str,
            author: str,
            date: str = r"\today"
    ) -> None:
        """doc_heading.

        :param title:
        :type title: str
        :param author:
        :type author: str
        :param date:
        :type date: str
        """
        logger.debug("Creating heading page")
        self.preamble.append(Command("title", title))
        self.preamble.append(Command("author", author))
        self.preamble.append(Command("date", NoEscape(date)))
        self.append(NoEscape(r"\maketitle"))

    def doc_append(self, *equations: str) -> None:
        """Append a sequence of experssions into the document.

        :param equations: the experssions to be added to the document.
        :type equations: str
        """
        logger.debug(f"Appending {equations}")
        with self.create(Alignat(numbering=True, escape=False)) as agn:
            for equation in equations:
                if equation is not None:
                    if isinstance(equation, str):
                        agn.append(equation)
                    else:
                        agn.extend(equation)

    def inte(self, equation: str) -> None:
        """inte.

        :param equation:
        :type equation: str
        """
        logger.debug(f"Integrating {equation}")
        solvable = True
        equation = sympify(equation)
        solution = trigsimp(simplify(integrate(equation, x)))
        # solution = integrate(trigsimp(simplify(equation)), x)
        eq_inte = Integral(equation, x)
        if str(eq_inte) == str(solution):
            solution = "No Computable Integral"
            solvable = False
        self.doc_append(
            latex(equation),
            r"=",
            latex(solution),
            r"+C" if solvable else None
        )
        return equation, solution

    def diff(self, equation: str) -> dict:
        """Differentiate an input equation.

        :param equation: in the form (x-variable experssions, order)
        :type equation: str
        :rtype: dict
        """
        logger.debug(f"Differentiating {equation}")
        eq_fmt = equation.split(",")
        equation = sympify(eq_fmt[0])
        order = int(eq_fmt[1]) if len(eq_fmt) == 2 else 1
        solution = simplify(diff(equation, x, order))
        eq_diff = Derivative(equation, x, order)
        self.doc_append(latex(eq_diff),
                        r"=",
                        latex(solution))
        return equation, order, solution

    def lim(self, equation: str) -> None:
        """lim.

        :param equation:
        :type equation: str
        """
        logger.debug(f"Findining limit of {equation}")
        eq_fmt = list(map(sympify, equation.split(",")))
        match len(eq_fmt):
            case 1:
                show, approach, sign = equation, 0, "+"
            case 2:
                show, approach, sign = eq_fmt[0], eq_fmt[1], "+"
            case 3:
                show, approach, sign = eq_fmt[0], eq_fmt[1], eq_fmt[2]
        solution = limit(show, x, approach, sign)
        if Limit(show, x, approach, sign) == solution:
            solution = "No Computable Limit"
        self.doc_append(latex(Limit(show, x, approach, sign)),
                        r"=", latex(solution))
        return show, approach, sign, solution

    def simp(self, equation: str) -> None:
        """simp.

        :param equation:
        :type equation: str
        """
        logger.debug(f"Simplifying {equation}")
        equation = sympify(equation)
        solution = trigsimp(simplify(equation))
        self.doc_append(latex(equation), r"=", latex(solution))
        return equation, solution

    def fact(self, equation: str) -> None:
        """fact.

        :param equation:
        :type equation: str
        """
        logger.debug(f"Factorizing {equation}")
        equation = sympify(equation)
        solution = factor(equation)
        solution = trigsimp(simplify(equation))
        self.doc_append(latex(equation), r"=", latex(solution))
        return equation, solution

    def sol(self, equation: str) -> None:
        """sol.

        :param equation:
        :type equation: str
        """
        logger.debug(f"Solving {equation} for x")
        if "=" in equation:
            eq_fmt = list(map(sympify, equation.split("=")))
            solution = solve(Eq(eq_fmt[0], eq_fmt[1]))
            is_x = True
        else:
            equation = sympify(equation)
            solution = solve(sympify(equation))
            is_x = False
        self.doc_append(
            latex(equation)
            if not is_x
            else rf"{latex(sympify(eq_fmt[0]))} = {latex(sympify(eq_fmt[1]))}",
            r"\Rightarrow",
            r"x=",
            latex(solution),
        )
        if is_x:
            return eq_fmt, solution
        return equation, solution

    def eval(self, equation: str) -> None:
        """eval.

        :param equation:
        :type equation: str
        """
        logger.debug(f"Evaluating {equation}")
        solution = sympify(eval(equation.replace("^", "**")))
        equation = sympify(equation, evaluate=False)
        self.doc_append(latex(equation), r"=", latex(solution))
        return equation, solution

    def plot(
        self,
        equation: str,
        height: str = "6cm",
        width: str = "6cm",
    ) -> None:
        """plot.

        :param equation:
        :type equation: str
        :param height:
        :type height: str
        :param width:
        :type width: str
        :param grid:
        :type grid: str
        :param axis_lines:
        :type axis_lines: str
        """
        logger.debug(f"Plotting {equation} in {width} w, {height} h")
        with self.create(Center()):
            with self.create(TikZ()):
                plot_options = f"height={height}, width={width}, \
                grid=both, axis lines=middle"
                with self.create(Axis(options=plot_options)) as plot:
                    plot.append(Plot(name=equation, func=equation))

    def matr(self, equation: str) -> None:
        """Matrix operations.

        Multiplication, addition, subtraction, determinant, etc.

        :equation: TODO
        :returns: TODO

        """
        logger.debug(f"Matrix {equation}")
        # multiplication
        if "*" in equation:
            logger.debug(f"Multiplication {equation}")

            eq_fmt = list(map(lambda a: matrix(eval(a)),
                              equation.split("*")))
            solution = reduce(mul, eq_fmt)
            show = list(map(Matrix, eq_fmt))
            self.doc_append(
                show,
                r"=",
                [Matrix(solution)]
            )
            return eq_fmt, show, solution
        # # division
        # if "/" in equation:
        #     eq_fmt = list(map(sympify, equation.split("/")))
        #     solution = eq_fmt[0] / eq_fmt[1]
        #     self.doc_append(
        #         latex(eq_fmt[0]),
        #         r"\div",
        #         latex(eq_fmt[1]),
        #         r"=",
        #         latex(solution)
        #     )
        #     return eq_fmt, solution
        # # addition
        # if "+" in equation:
        #     eq_fmt = list(map(sympify, equation.split("+")))
        #     solution = eq_fmt[0] + eq_fmt[1]
        #     self.doc_append(
        #         latex(eq_fmt[0]),
        #         r"+",
        #         latex(eq_fmt[1]),
        #         r"=",
        #         latex(solution)
        #     )
        #     return eq_fmt, solution
        # # subtraction
        # if "-" in equation:
        #     eq_fmt = list(map(sympify, equation.split("+")))
        #     solution = eq_fmt[0] - eq_fmt[1]
        #     self.doc_append(
        #         latex(eq_fmt[0]),
        #         r"-",
        #         latex(eq_fmt[1]),
        #         r"=",
        #         latex(solution)
        #     )
        #     return eq_fmt, solution
        # # determinant
        # if "det" in equation:
        #     eq_fmt = list(map(sympify, equation.split("det")))
        #     solution = det(eq_fmt[0])
        #     self.doc_append(
        #         latex(eq_fmt[0]),
        #         r"det",
        #         r"=",
        #         latex(solution)
        #     )
        #     return eq_fmt, solution
        # # inverse
        # if "inv" in equation:
        #     eq_fmt = list(map(sympify, equation.split("inv")))
        #     solution = inv(eq_fmt[0])
        #     self.doc_append(
        #         latex(eq_fmt[0]),
        #         r"inv",
        #         r"=",
        #         latex(solution)
        #     )
        #     return eq_fmt, solution
        # # transpose
        # if "T" in equation:
        #     eq_fmt = list(map(sympify, equation.split("T")))
        #     solution = eq_fmt[0].T
        #     self.doc_append(
        #         latex(eq_fmt[0]),
        #         r"T",
        #         r"=",
        #         latex(solution)
        #     )
        #     return eq_fmt, solution


if __name__ == "__main__":
    # geometry_options = {"tmargin": "1cm", "lmargin": "10cm"}
    doc = MathDocument()
    FILE = "full"

    # logger.disable("__main__")

    doc.doc_heading(title="Func.Py Tests", author="SalahDin Rezk")
    doc.matr("[[1,2],[3,4]]*[[1,2],[3,4]]")

    doc.generate_pdf(FILE, clean_tex=True)
