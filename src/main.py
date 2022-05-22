from __future__ import division

import logging

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore
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
            getattr(self, f"{op}Bt").setShortcut(shortcut)
        self.expTxt.setFocus()

    def exceptHook(self, exc_type, exc_value, exc_traceback):
        """Exceptions hook to be shown

        :exc_type: TODO
        :exc_value: TODO
        :exc_traceback: TODO
        :returns: TODO

        """
        from traceback import format_tb

        logging.error(f"Exception Type: {exc_type}")
        logging.error(f"Exception Value: {exc_value}")
        logging.error(f"Exception Traceback: {format_tb(exc_traceback)}")

        errorbox = QtWidgets.QMessageBox()
        errorbox.setText(f"""Error:
        \n{exc_type}
        \n{exc_value}
        \n{format_tb(exc_traceback)}
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
        exec(f"""
            \n@QtCore.pyqtSlot()
            \ndef on_{func}Bt_clicked(self):
            \n    self.mathdoc.{func}(self.expTxt.toPlainText().replace(" ", ""))
        """)

    def headingFunc(self):
        self.mathdoc.Heading(
            self.titleTxt.toPlainText(),
            self.authorTxt.toPlainText(),
        )

    @QtCore.pyqtSlot()
    def on_genPdfBt_clicked(self):
        self.headingFunc()
        self.mathdoc.generate_pdf(
            self.fileTxt.text(),
            clean_tex=True
        )

    @QtCore.pyqtSlot()
    def on_genLatexBt_clicked(self):
        self.headingFunc()
        self.mathdoc.generate_tex(self.fileTxt.text())


if __name__ == "__main__":
    import sys

    level = logging.DEBUG
    fmt = "[%(levelname)s] %(asctime)s - %(funcName)s|%(message)s"
    logging.basicConfig(level=level, format=fmt)

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
