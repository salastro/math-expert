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

    def Heading(self, title, author, date=r"\today"):
        self.preamble.append(Command("title", title))
        self.preamble.append(Command("author", author))
        self.preamble.append(Command("date", NoEscape(date)))
        self.append(NoEscape(r"\maketitle"))

    def GenPdf(self, file, title, author, date=r"\today", clean_tex=True):
        self.Heading(title, author, date)
        self.generate_pdf(file, clean_tex=clean_tex)

    def GenTex(self, file, title, author, date=r"\today"):
        self.Heading(title, author, date)
        self.generate_tex(file)

    def Inte(self, equation):
        try:
            solvable = True
            equation = sympify(equation)
            solution = trigsimp(simplify(integrate(equation, x)))
            # solution = integrate(trigsimp(simplify(equation)), x)
            equation = Integral(equation, x)
            print(equation, solution)
            if equation == solution:
                solution = "No computable integral"
                solvable = False
                print("no computable integral")
            with self.create(Alignat(numbering=True, escape=False)) as agn:
                agn.append(latex(equation))
                agn.append(r"=")
                agn.append(latex(solution))
                agn.append(r"+C") if solvable else None
        except:
            error_message()

    def Diff(self, equation):
        try:
            eq = equation.split(",")
            equation = sympify(eq[0])
            n = int(eq[1]) if len(eq) == 2 else 1
            solution = equation
            for _ in range(n):
                solution = simplify(diff(solution, x))
                equation = Derivative(equation, x)
            with self.create(Alignat(numbering=True, escape=False)) as agn:
                agn.append(latex(equation))
                agn.append(r"=")
                agn.append(latex(solution))
        except:
            error_message()

    def Lim(self, equation):
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
            with self.create(Alignat(numbering=True, escape=False)) as agn:
                agn.append(latex(Limit(show, x, a, s)))
                agn.append(r"=")
                agn.append(latex(solution))
        except:
            error_message()

    def Simp(self, equation):
        try:
            equation = sympify(equation)
            solution = trigsimp(simplify(equation))
            with self.create(Alignat(numbering=True, escape=False)) as agn:
                agn.append(latex(equation))
                agn.append(r"=")
                agn.append(latex(solution))
        except:
            error_message()

    def Fact(self, equation):
        try:
            equation = sympify(equation)
            solution = factor(equation)
            with self.create(Alignat(numbering=True, escape=False)) as agn:
                agn.append(latex(equation))
                agn.append(r"=")
                agn.append(latex(solution))
        except:
            error_message()

    def Sol(self, equation):
        try:
            if "=" in equation:
                eq = equation.split("=")
                solution = solve(Eq(sympify(eq[0]), sympify(eq[1])))
                x_ = True
            else:
                equation = sympify(equation)
                solution = solve(sympify(equation))
                x_ = False
            with self.create(Alignat(numbering=True, escape=False)) as agn:
                if not x_:
                    agn.append(latex(equation))
                else:
                    agn.append(latex(sympify(eq[0])))
                    agn.append(r"=")
                    agn.append(latex(sympify(eq[1])))
                agn.append(r"\Rightarrow")
                agn.append(r"x=") if x_ else None
                agn.append(latex(solution))
        except:
            error_message()

    def Eval(self, equation):
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

            solution = eval(equation.replace("^", "**"))
            equation = sympify(equation, evaluate=False)
            # solution = eval(equation)
            with self.create(Alignat(numbering=True, escape=False)) as agn:
                agn.append(latex(equation))
                agn.append(r"=")
                agn.append(latex(solution))
        except:
            error_message()

    def Plot(
        self, equation, height="6cm", width="6cm", grid="both", axis_lines="middle"
    ):
        try:
            with self.create(Center()):
                with self.create(TikZ()):
                    plot_options = f"height={height}, width={width}, grid={grid}, axis lines={axis_lines}"
                    with self.create(Axis(options=plot_options)) as plot:
                        plot.append(Plot(name=equation, func=equation))
        except:
            error_message()


if __name__ == "__main__":
    # geometry_options = {"tmargin": "1cm", "lmargin": "10cm"}
    doc = MathDoc()
    file_name = "full"

    doc.Heading(title="Integral Homework", author="SalahDin Rezk")
    from sympy import cos, sin

    doc.Inte((sin(x) ** 2 - cos(x) ** 2) / (cos(x) ** 2 * sin(x) ** 2))
    doc.Diff("x**x")
    doc.Diff("x**x, 2")
    doc.Diff("x**(1/x), 2")
    doc.Lim("2/sin(2*x),oo")
    doc.Sol("x+3=1")
    doc.Sol("x+3>1")
    doc.Eval("2^2")
    doc.Eval("sqrt(2)")
    doc.Eval("sin(2)")
    doc.Eval("sin(45/cos(3))")
    # doc.Eval('(3i+5)-(10i+5)')

    doc.generate_pdf(file_name, clean_tex=True)
