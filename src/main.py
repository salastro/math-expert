from __future__ import division

from PyQt5.QtWidgets import QMainWindow
from sympy import (acos, asin, atan, cos, cot, csc, dsolve, exp, ln, log, oo,
                   pi, sec, sin, sqrt, symbols, sympify, tan)
from sympy.abc import x

from func import MathDoc
from gui import QtWidgets, Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        sys.excepthook = self.exceptHook
        self.setupUi(self)
        self.mathdoc = MathDoc()
        self.headingFunc()
        self.inteBt.clicked.connect(self.inteFunc)
        self.diffBt.clicked.connect(self.diffFunc)
        self.limBt.clicked.connect(self.limFunc)
        self.simpBt.clicked.connect(self.simpFunc)
        self.factBt.clicked.connect(self.factFunc)
        self.solBt.clicked.connect(self.solFunc)
        self.plotBt.clicked.connect(self.plotFunc)
        self.evalBt.clicked.connect(self.evalFunc)
        self.genPdfBt.clicked.connect(self.genPdfFunc)
        self.genLatexBt.clicked.connect(self.genLatexFunc)

    def exceptHook(self, exc_type, exc_value, exc_traceback):
        """Exceptions hook to be shown

        :exc_type: TODO
        :exc_value: TODO
        :exc_traceback: TODO
        :returns: TODO

        """
        errorbox = QtWidgets.QMessageBox()
        errorbox.setText(f"""Error:
        \n{exc_type}
        \n{exc_value}
        \n{exc_traceback}
        """)
        errorbox.exec_()

    def inteFunc(self):
        self.mathdoc.Inte(self.expTxt.toPlainText().replace(" ", ""))

    def diffFunc(self):
        self.mathdoc.Diff(self.expTxt.toPlainText().replace(" ", ""))

    def limFunc(self):
        self.mathdoc.Lim(self.expTxt.toPlainText().replace(" ", ""))

    def simpFunc(self):
        self.mathdoc.Simp(self.expTxt.toPlainText().replace(" ", ""))

    def factFunc(self):
        self.mathdoc.Fact(self.expTxt.toPlainText().replace(" ", ""))

    def solFunc(self):
        self.mathdoc.Sol(self.expTxt.toPlainText().replace(" ", ""))

    def plotFunc(self):
        self.mathdoc.Plot((self.expTxt.toPlainText().replace(" ", "")))

    def evalFunc(self):
        self.mathdoc.Eval((self.expTxt.toPlainText().replace(" ", "")))

    def headingFunc(self):
        self.mathdoc.Heading(
            self.titleTxt.toPlainText(),
            self.authorTxt.toPlainText(),
        )

    def genPdfFunc(self):
        self.headingFunc()
        self.mathdoc.generate_pdf(
            self.fileTxt.toPlainText(),
            clean_tex=True
        )

    def genLatexFunc(self):
        self.headingFunc()
        self.mathdoc.generate_tex(self.fileTxt.toPlainText())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
