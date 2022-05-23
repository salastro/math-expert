from __future__ import division

from loguru import logger
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow

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

    operations = ["inte", "diff", "lim", "fact", "sol",
                  "simp", "eval", "plot", "genPdf", "genLatex"]

    for func in operations:
        exec(f"""
            \n@pyqtSlot()
            \ndef on_{func}Bt_clicked(self):
            \n    self.mathdoc.{func}(self.expTxt.toPlainText().replace(" ", \
                ""))
        """)

    def exceptHook(self, exc_type, exc_value, exc_traceback):
        """Exceptions hook to be shown

        :exc_type: TODO
        :exc_value: TODO
        :exc_traceback: TODO
        :returns: TODO

        """
        from traceback import format_tb

        logger.error(f"Exception Type: {exc_type}")
        logger.error(f"Exception Value: {exc_value}")
        logger.error(f"Exception Traceback: {format_tb(exc_traceback)}")

        errorbox = QtWidgets.QMessageBox()
        errorbox.setText(f"""Error:
                \n{exc_type}
                \n{exc_value}
                \n{format_tb(exc_traceback)}
                """)
        errorbox.exec_()

    def headingFunc(self):
        self.mathdoc.doc_heading(
            self.titleTxt.toPlainText(),
            self.authorTxt.toPlainText(),
        )

    @pyqtSlot()
    def on_genPdfBt_clicked(self):
        self.headingFunc()
        self.mathdoc.generate_pdf(
            self.fileTxt.text(),
            clean_tex=True
        )

    @pyqtSlot()
    def on_genLatexBt_clicked(self):
        self.headingFunc()
        self.mathdoc.generate_tex(self.fileTxt.text())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
