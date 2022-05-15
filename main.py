from __future__ import division

from sympy import (
    Derivative,
    Eq,
    Function,
    acos,
    asin,
    atan,  # common math
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
from gui import QtWidgets, Ui_MainWindow  # gui

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    math_doc = MathDoc()
    ui.inteBt.clicked.connect(
        lambda: math_doc.Inte(ui.expTxt.toPlainText().replace(" ", ""))
    )
    ui.diffBt.clicked.connect(
        lambda: math_doc.Diff(ui.expTxt.toPlainText().replace(" ", ""))
    )
    ui.limBt.clicked.connect(
        lambda: math_doc.Lim(ui.expTxt.toPlainText().replace(" ", ""))
    )
    ui.simpBt.clicked.connect(
        lambda: math_doc.Simp(ui.expTxt.toPlainText().replace(" ", ""))
    )
    ui.factBt.clicked.connect(
        lambda: math_doc.Fact(ui.expTxt.toPlainText().replace(" ", ""))
    )
    ui.solBt.clicked.connect(
        lambda: math_doc.Sol(ui.expTxt.toPlainText().replace(" ", ""))
    )
    ui.plotBt.clicked.connect(
        lambda: math_doc.Plot((ui.expTxt.toPlainText().replace(" ", "")))
    )
    ui.evalBt.clicked.connect(
        lambda: math_doc.Eval((ui.expTxt.toPlainText().replace(" ", "")))
    )
    ui.genPdfBt.clicked.connect(
        lambda: math_doc.GenPdf(
            ui.fileTxt.toPlainText(),
            ui.titleTxt.toPlainText(),
            ui.authorTxt.toPlainText(),
            clean_tex=True,
        )
    )
    ui.genLatexBt.clicked.connect(
        lambda: math_doc.GenTex(
            ui.fileTxt.toPlainText(),
            ui.titleTxt.toPlainText(),
            ui.authorTxt.toPlainText(),
        )
    )

    MainWindow.show()
    sys.exit(app.exec_())
