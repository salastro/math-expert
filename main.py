from __future__ import division

from sympy import (Derivative, Eq, Function, acos, asin, atan,  # common math
                   cos, cot, csc, dsolve, exp, ln, log, oo, pi, sec, sin, sqrt,
                   symbols, sympify, tan)
from sympy.abc import x

from func import MathDoc
from gui import QtWidgets, Ui_MainWindow  # gui

if __name__ == "__main__":
    # Setup the ui.
    import sys  # for command line arguments
    app = QtWidgets.QApplication(sys.argv)  # Create the application.
    MainWindow = QtWidgets.QMainWindow()  # Create the main window.
    ui = Ui_MainWindow()  # Create the ui.
    ui.setupUi(MainWindow)  # Setup the ui.

    # Setup the document and buttons.
    math_doc = MathDoc()  # The document.
    ui.inteBt.clicked.connect(lambda: math_doc.Inte(
        ui.expTxt.toPlainText().replace(' ', '')))
    ui.diffBt.clicked.connect(lambda: math_doc.Diff(
        ui.expTxt.toPlainText().replace(' ', '')))
    ui.limBt.clicked.connect(lambda: math_doc.Lim(
        ui.expTxt.toPlainText().replace(' ', '')))
    ui.simpBt.clicked.connect(lambda: math_doc.Simp(
        ui.expTxt.toPlainText().replace(' ', '')))
    ui.factBt.clicked.connect(lambda: math_doc.Fact(
        ui.expTxt.toPlainText().replace(' ', '')))
    ui.solBt.clicked.connect(lambda: math_doc.Sol(
        ui.expTxt.toPlainText().replace(' ', '')))
    ui.plotBt.clicked.connect(lambda: math_doc.Plot(
        (ui.expTxt.toPlainText().replace(' ', ''))))
    ui.evalBt.clicked.connect(lambda: math_doc.Eval(
        (ui.expTxt.toPlainText().replace(' ', ''))))
    ui.genPdfBt.clicked.connect(lambda: math_doc.GenPdf(ui.fileTxt.toPlainText(
        ), ui.titleTxt.toPlainText(), ui.authorTxt.toPlainText(),
        clean_tex=True))
    ui.genLatexBt.clicked.connect(lambda: math_doc.GenTex(ui.fileTxt.toPlainText(
        ), ui.titleTxt.toPlainText(),
        ui.authorTxt.toPlainText()))  # The generate tex button.

    MainWindow.show()
    sys.exit(app.exec_())
