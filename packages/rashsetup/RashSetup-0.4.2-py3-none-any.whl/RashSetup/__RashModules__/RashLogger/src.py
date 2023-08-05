from PySide2 import QtCore, QtGui, QtWidgets
import logging
from RashSetup.shared import LockOut, LockErr, LogHandler
import pathlib

__all__ = [
    "LogWindow"

]


class FD(QtWidgets.QTextBrowser):
    flow_out = QtCore.Signal(str)
    flow_err = QtCore.Signal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.flow_err.connect(self.pipe_err)
        self.flow_out.connect(self.pipe_out)

        self.err = LockErr(self.flow_err.emit)
        self.out = LockOut(self.flow_out.emit)

        self.document().setDefaultStyleSheet(
            (
                    pathlib.Path(__file__).parent / "design.css"
            ).read_text()
        )

    def pipe_out(self, text):
        self.insertHtml(
            (
                    pathlib.Path(__file__).parent / "format.html"
            ).read_text().format(
                "CONSOLE_OUT", "from stdout", text.replace("<", "&lt;").replace(">", "&gt;")
            )
        )

    def pipe_err(self, text):
        self.insertHtml(
            (
                    pathlib.Path(__file__).parent / "format.html"
            ).read_text().format(
                "CONSOLE_ERR", "from stderr", text.replace("<", "&lt;").replace(">", "&gt;")
            )
        )



class LogProcess(QtWidgets.QTextBrowser):
    Print = QtCore.Signal(str, logging.LogRecord)
    SetTitle = QtCore.Signal(str)

    def __init__(self, parent, logger: logging.Logger, handler=None):
        super().__init__(parent)

        self.Print.connect(self.print_log)

        self.handler = handler if handler else LogHandler(
            self.Print.emit
        )

        None if self.handler.callback else self.handler.register_callback(self.Print.emit)

        logger.addHandler(self.handler)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False

        self.name, self.pid = "NOT SET", -2
        self.emit_tit()

        self.document().setDefaultStyleSheet(
            (pathlib.Path(__file__).parent / "design.css").read_text()
        )

    def print_log(self, text, record: logging.LogRecord):
        self.insertHtml(
            (
                    pathlib.Path(__file__).parent / "log_format.html"
            ).read_text().format(
                record.levelname,
                record.thread,
                record.threadName,
                record.pathname,
                record.lineno,
                record.funcName,
                record.relativeCreated,
                text
            )
        )

    def setName(self, name):
        self.emit_tit()

    def setPid(self, name):
        self.emit_tit()

    def emit_tit(self):
        return self.SetTitle.emit(f"{self.name}[{self.pid}]")


class LogWindow(QtWidgets.QTabWidget):
    AddProcess = QtCore.Signal(logging.Logger, logging.Handler)

    def __init__(self, parent):
        super().__init__(parent)

        self.rash_process = LogProcess(
            self, logging.getLogger("")
        )

        self.addTab(
            self.rash_process, "Root"
        )

        self.addTab(
            FD(self), "Pipes"
        )

        self.AddProcess.connect(self.add_process)

    def add_process(self, logger: logging.Logger, handler: LogHandler):
        process = LogProcess(self, logger, handler)

        self.addTab(
            process, "README"
        )

        setattr(handler, "__switch", lambda: self.setCurrentWidget(process))

    def __call__(self):
        return self.rash_logger


class LogTab(QtWidgets.QTabBar):
    def __init__(self, parent):
        super().__init__(parent)


if __name__ == "__main__":
    check = QtWidgets.QApplication([])

    sample = FD(None)
    sample.show()

    check.exec_()
