from sympy import cos, exp, integrate, sqrt, diff
from sympy.integrals.manualintegrate import manualintegrate
from sympy.integrals.risch import NonElementaryIntegral
from sympy.abc import x
from sympy.printing import latex

from pylatex import Document, Section, Subsection, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat, Command, Center
from pylatex.utils import NoEscape


class MathDoc(Document):
    def __init__(self):
        super().__init__()
        # TODO: add preamble change gemotry

    def Heading(self, title, author, date=r'\today'):
        self.preamble.append(Command('title', title))
        self.preamble.append(Command('author', author))
        self.preamble.append(Command('date', NoEscape(date)))
        self.append(NoEscape(r'\maketitle'))

    def GenPdf(self, file, title, author, date=r'\today', clean_tex=True):
        self.Heading(title, author, date)
        self.generate_pdf(file, clean_tex=clean_tex)

    def GenTex(self, file, title, author, date=r'\today'):
        self.Heading(title, author, date)
        self.generate_tex(file)

    def Inte(self, problem):
        solution = manualintegrate(problem, x)
        if isinstance(integrate(problem.rewrite(cos, exp), x, risch=True),
                      NonElementaryIntegral):
            solution = 'Non-elementary'
        with self.create(Alignat(numbering=True, escape=False)) as agn:
            agn.append(r'\int')
            agn.append(latex(problem))
            agn.append(r'\, dx')
            agn.append(r'=')
            agn.append(latex(solution))
            agn.append(r'+C')

    def Diff(self, problem, n=1):
        solution = problem
        for _ in range(n):
            solution = diff(solution, x)
        with self.create(Alignat(numbering=True, escape=False)) as agn:
            if n == 1:
                agn.append(r'\frac{d}{dx}')
            else:
                agn.append(r'\frac{d^'+str(n)+'}{dx^'+str(n)+'}')
            agn.append(latex(problem))
            agn.append(r'=')
            agn.append(latex(solution))

    def Plot(self, equation, height='4cm', width='6cm',
             grid='both', axis_lines='middle'):
        with self.create(Center()):
            with self.create(TikZ()):
                plot_options = f'height={height}, width={width}, grid={grid}, axis lines={axis_lines}'
                with self.create(Axis(options=plot_options)) as plot:
                    plot.append(Plot(name=equation, func=equation))


if __name__ == '__main__':
    # geometry_options = {"tmargin": "1cm", "lmargin": "10cm"}
    doc = MathDoc()
    file_name = 'full'

    doc.Heading(title='Integral Homework', author='SalahDin Rezk')
    doc.Inte(x/sqrt(1-3*x))
    doc.Inte(1/sqrt(1-3*x))
    doc.Inte(x**x)
    doc.Diff(x**x)
    doc.Diff(x**x, 2)
    doc.Diff(x**(1/x), 2)

    doc.generate_pdf(file_name, clean_tex=True)
