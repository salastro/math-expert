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
        for op, shortcut in self.operations.items():
            exec(f"""
                \nself.{op}Bt.clicked.connect(self.{op}Func)
                \nself.{op}Bt.setShortcut("{shortcut}")
            """)

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

    operations = {
        "inte": "Ctrl+I",
        "diff": "Ctrl+D",
        "lim": "Ctrl+L",
        "fact": "Ctrl+F",
        "sol": "Ctrl+S",
        "simp": "Alt+S",
        "eval": "Ctrl+E",
        "plot": "Ctrl+P",
        "genPdf": "Ctrl+Return",
        "genLatex": "Alt+Return"
    }
    for func in operations:
        if func not in ["genPdf", "genLatex"]:
            exec(f"""
                \ndef {func}Func(self):
                \n    self.mathdoc.{func}(self.expTxt.toPlainText().replace(" ", ""))
            """)

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
    fmt = "[%(levelname)s] %(asctime)s - %(funcName)s|%(message)s"
    logging.basicConfig(level=level, format=fmt)

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
