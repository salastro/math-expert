from __future__ import division

from pylatex import Alignat, Axis, Center, Command, Document, Plot, TikZ

# Section, Subsection, Math, Figure, Matrix,
from pylatex.utils import NoEscape
from sympy import (
    Derivative,
    Eq,
    Integral,
    Limit,
    diff,
    factor,
    integrate,
    limit,
    oo,
    simplify,
    solve,
    sqrt,
    sympify,
    trigsimp,
)

# from sympy.integrals.manualintegrate import manualintegrate, integral_steps
# from sympy.integrals.risch import NonElementaryIntegral
from sympy.abc import x
from sympy.printing import latex

from err import QtWidgets
from err import Ui_Dialog as Form


def error_message():
    dialog = QtWidgets.QDialog()
    dialog.ui = Form()
    dialog.ui.setupUi(dialog)
    dialog.exec_()
    dialog.show()


class MathDoc(Document):
    def __init__(self):
        super().__init__()
        # TODO: add preamble change gemotry

    def Heading(self, title: str, author: str, date: str = r"\today") -> None:
        self.preamble.append(Command("title", title))
        self.preamble.append(Command("author", author))
        self.preamble.append(Command("date", NoEscape(date)))
        self.append(NoEscape(r"\maketitle"))

    def GenPdf(
        self,
        file: str,
        title: str,
        author: str,
        date: str = r"\today",
        clean_tex: bool = True,
    ) -> None:
        self.Heading(title, author, date)
        self.generate_pdf(file, clean_tex=clean_tex)

    def GenTex(self, file: str, title: str, author: str, date: str = r"\today") -> None:
        self.Heading(title, author, date)
        self.generate_tex(file)

    def Append(self, *equations: str) -> None:
        """Append a sequence of experssions into the document

        :*equations: the experssions to be added to the document
        :returns: None

        """
        with self.create(Alignat(numbering=True, escape=False)) as agn:
            for equation in equations:
                agn.append(equation) if equation is not None else None

    def Inte(self, equation: str) -> None:
        try:
            solvable = True
            equation = sympify(equation)
            solution = trigsimp(simplify(integrate(equation, x)))
            # solution = integrate(trigsimp(simplify(equation)), x)
            equation = Integral(equation, x)
            print(equation, solution)
            if str(equation) == str(solution):
                solution = "No computable integral"
                solvable = False
                print("no computable integral")
            self.Append(latex(equation), r"=", latex(solution), r"+C" if solvable else None)
        except Exception:
            error_message()

    def Diff(self, equation: str) -> None:
        try:
            eq = equation.split(",")
            equation = sympify(eq[0])
            n = int(eq[1]) if len(eq) == 2 else 1
            solution = equation
            for _ in range(n):
                solution = simplify(diff(solution, x))
                equation = Derivative(equation, x)
            self.Append(latex(equation), r"=", latex(solution))
        except Exception:
            error_message()

    def Lim(self, equation: str) -> None:
        try:
            eq = equation.split(",")
            match len(eq):
                case 1:
                    show, a, s = equation, 0, "+"
                case 2:
                    show, a, s = eq[0], eq[1], "+"
                case 3:
                    show, a, s = eq[0], eq[1], eq[2]
            solution = limit(sympify(show), x, sympify(a), s)
            if Limit(show, x, a, s) == solution:
                solution = "No computable limit"
                print("no computable limit")
            print(eq, solution, show, sep="\n")
            self.Append(latex(Limit(show, x, a, s)), r"=", latex(solution))
        except Exception:
            error_message()

    def Simp(self, equation: str) -> None:
        try:
            equation = sympify(equation)
            solution = trigsimp(simplify(equation))
            self.Append(latex(equation), r"=", latex(solution))
        except Exception:
            error_message()

    def Fact(self, equation: str) -> None:
        try:
            equation = sympify(equation)
            solution = factor(equation)
            self.Append(latex(equation), r"=", latex(solution))
        except Exception:
            error_message()

    def Sol(self, equation: str) -> None:
        try:
            if "=" in equation:
                eq = equation.split("=")
                solution = solve(Eq(sympify(eq[0]), sympify(eq[1])))
                x_ = True
            else:
                equation = sympify(equation)
                solution = solve(sympify(equation))
                x_ = False
            self.Append(
                latex(equation) if not x_
                else rf"{latex(sympify(eq[0]))} = {latex(sympify(eq[1]))}",
                r"\Rightarrow",
                r"x=",
                latex(solution)
            )
        except Exception:
            error_message()

    def Eval(self, equation: str) -> None:
        try:
            from numpy import (
                arccos,
                arcsin,
                arctan,
                cos,
                exp,
                log,
                log10,
                pi,
                sin,
                sqrt,
                tan,
            )

            solution = sympify(eval(equation.replace("^", "**")))
            equation = sympify(equation, evaluate=False)
            # solution = eval(equation)
            self.Append(latex(equation), r"=", latex(solution))
        except Exception:
            error_message()

    def Plot(
        self,
        equation: str,
        height: str = "6cm",
        width: str = "6cm",
        grid: str = "both",
        axis_lines: str = "middle",
    ) -> None:
        try:
            with self.create(Center()):
                with self.create(TikZ()):
                    plot_options = f"height={height}, width={width}, grid={grid}, axis lines={axis_lines}"
                    with self.create(Axis(options=plot_options)) as plot:
                        plot.append(Plot(name=equation, func=equation))
        except Exception:
            error_message()


if __name__ == "__main__":
    # geometry_options = {"tmargin": "1cm", "lmargin": "10cm"}
    doc = MathDoc()
    file_name = "full"

    doc.Heading(title="Func.Py Tests", author="SalahDin Rezk")
    from sympy import cos, sin

    doc.Inte("(sin(x) ** 2 - cos(x) ** 2) / (cos(x) ** 2 * sin(x) ** 2)")
    doc.Inte("x^x")
    doc.Diff("x**(1/x)")
    doc.Diff("x**(1/x), 2")
    doc.Lim("2/sin(2*x),oo")
    doc.Lim("(sin(x)^2 - cos(x)^2) / (cos(x)^2 * sin(x)^2), oo")
    doc.Sol("x+3=1")
    doc.Sol("x+3>1")
    doc.Eval("2^2")
    doc.Eval("sqrt(2)")
    doc.Eval("sin(2)")
    doc.Eval("sin(45/cos(3))")
    doc.Eval('sin(1j)')

    doc.generate_pdf(file_name, clean_tex=True)
