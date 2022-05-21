from __future__ import division

import logging

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
        self.expTxt.setFocus()
        self.inteBt.clicked.connect(self.inteFunc)
        self.inteBt.setShortcut("Ctrl+I")
        self.diffBt.clicked.connect(self.diffFunc)
        self.diffBt.setShortcut("Ctrl+D")
        self.limBt.clicked.connect(self.limFunc)
        self.limBt.setShortcut("Ctrl+L")
        self.simpBt.clicked.connect(self.simpFunc)
        self.simpBt.setShortcut("Alt+S")
        self.factBt.clicked.connect(self.factFunc)
        self.factBt.setShortcut("Ctrl+F")
        self.solBt.clicked.connect(self.solFunc)
        self.solBt.setShortcut("Ctrl+S")
        self.plotBt.clicked.connect(self.plotFunc)
        self.plotBt.setShortcut("Ctrl+P")
        self.evalBt.clicked.connect(self.evalFunc)
        self.evalBt.setShortcut("Ctrl+E")
        self.genPdfBt.clicked.connect(self.genPdfFunc)
        self.genPdfBt.setShortcut("Ctrl+Return")
        self.genLatexBt.clicked.connect(self.genLatexFunc)
        self.genLatexBt.setShortcut("Alt+Return")

    def exceptHook(self, exc_type, exc_value, exc_traceback):
        """Exceptions hook to be shown

        :exc_type: TODO
        :exc_value: TODO
        :exc_traceback: TODO
        :returns: TODO

        """
        logging.error(f"Exception Type: {exc_type}")
        logging.error(f"Exception Value: {exc_value}")
        logging.error(f"Exception Traceback: {exc_traceback}")

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

    level = logging.DEBUG
    fmt = '[%(levelname)s] %(asctime)s - %(funcName)s|%(message)s'
    logging.basicConfig(level=level, format=fmt)

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
