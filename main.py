from __future__ import division

from sympy import (
    acos,
    asin,
    atan,
    cos,
    cot,
    csc,
    dsolve,
    exp,
    ln,
    log,
    oo,
    pi,
    sec,
    sin,
    sqrt,
    symbols,
    sympify,
    tan,
)
from sympy.abc import x

from func import MathDoc
from gui import QtWidgets, Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
# from err import Ui_Dialog


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
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

    # def ErrorMessage(func):
    #     # dialog = QtGui.QDialog()
    #     dialog = Ui_Dialog()
    #     dialog.setupUi(dialog)
    #     dialog.exec_()
    #     dialog.show()
        
    # @ErrorMessage
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

    # @ErrorMessage
    def genLatexFunc(self):
        self.headingFunc()
        self.mathdoc.generate_tex(self.fileTxt.toPlainText())

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
