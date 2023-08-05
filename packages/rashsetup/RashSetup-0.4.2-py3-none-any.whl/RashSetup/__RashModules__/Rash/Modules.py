import logging.handlers
import multiprocessing
import threading
from PySide2 import QtWidgets, QtCore, QtGui
import webbrowser
import os
import traceback
import sys

from .src import *


class Misc:
    Current = pathlib.Path(__file__).parent
    Misc = Current / "Misc"
    Gifs = Misc / "Gifs"
    Icons = Misc / "Icons"
    Logs = Misc / "Logs"
    Settings = os.path.join(os.path.dirname(__file__), "settings.json")
    CMD = os.path.join(os.path.dirname(sys.executable), "RashCMD.exe")

    @staticmethod
    def ensure_paths():
        None if Misc.Logs.exists() else Misc.Logs.mkdir()


def FormatException(traceback_: Exception, raw=False):
    file = Misc.Misc / "HTML" / "ShowException.html"

    parser = traceback.TracebackException(
        type(traceback_), traceback_, traceback_.__traceback__
    )

    if raw:
        return QtWidgets.QApplication.clipboard().setText(
            parser.exc_type.__name__ + "\n" + ''.join(parser.stack.format())
        )

    return file.read_text().format(
        parser.exc_type.__name__,
        str(parser)
    ), ''.join(parser.stack.format())


class GifMovie(QtGui.QMovie):
    def __init__(self, gif, parent, ratio=None):
        super().__init__(str(gif))
        self.setParent(parent)
        self.ratio = ratio
        self.frameChanged.connect(self.release_pix)
        self.start()

    def release_pix(self):
        play = self.currentPixmap()
        play = play.scaled(play.size() / self.ratio)

        play.setDevicePixelRatio(3)
        self.parent().setPixmap(play)

    def running(self):
        return QtGui.QMovie.Running == self.MovieState


class GifPlayer(QtWidgets.QLabel):
    def __init__(self, parent, gif, ratio):
        super().__init__(parent)

        self.gif = GifMovie(gif, self, ratio)

    def start(self):
        self.gif.start()

    def stop(self):
        self.gif.stop()


class ClickLabel(QtWidgets.QLabel):
    clicked = QtCore.Signal()
    double_clicked = QtCore.Signal()
    enter = QtCore.Signal()
    leave = QtCore.Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._movie = None
        self._ratio = StatusBar.Ratio
        self.setObjectName("ClickLabel")

    def mousePressEvent(self, event):
        self.clicked.emit()
        return super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:
        self.double_clicked.emit()

        return super().mouseDoubleClickEvent(event)

    def enterEvent(self, event):
        self.enter.emit()

        return super().enterEvent(event)

    def leaveEvent(self, event):
        self.leave.emit()

        return super().leaveEvent(event)

    def load_gif(self, gif: str, ratio=None):
        self._movie = self._movie.setFileName(gif) if self._movie else GifMovie(gif, self, ratio)

    def movie(self):
        return self._movie


class ReloadButton(ClickLabel):
    def __init__(self, parent, gif):
        super().__init__(parent)

        self.normal = gif, 19
        self.load_gif(*self.normal)

        self.movie().stop()

        self.mode = 0
        # 0 means free
        # 1 means loading
        # 2 means ready if there's an update

        self.enter.connect(lambda: self.toggle(1))
        self.leave.connect(lambda: self.toggle(0))
        self.clicked.connect(self.take_action)

        self.set_tips()

    def set_tips(self, normal=True):
        self.setStatusTip("Checks for updates !" if normal else "Checking for Updates!")
        self.setToolTip("Check update ?" if normal else "Scraping!")

    def toggle(self, result):
        if self.mode != 0:
            return

        self.movie().start() if result else self.movie().stop()

    def load(self):
        self.mode = 1
        self.set_tips(False)

        self.load_gif(str(Misc.Gifs / "loading.gif"), 6)
        crawler = SettingsCrawler()
        handler = JsonHandler(Misc.Settings).load()

        thread = SafeThread(
            self,
            "UpdaterCheckerThread",
            crawler,
            False,
            True,
            {
                handler["general"]["name"]: [handler["general"]["hosted"], str(Misc.Settings)]
            },
            lambda x: self.collect(x, crawler.close)
        )

        thread.start()

    def collect(self, meta, close_it):
        open("test.txt", "w").write(meta["Rash"]["update"])

        self.mode = 1
        self.set_tips()
        self.load_gif(*self.normal)

    def display_results(self, meta):
        self.setStatusTip(meta["title"])
        self.setToolTip(
            f"<h1> {meta['title']} </h1>"
            f"{meta['']}"
        )

    def take_action(self):
        try:
            self.load() if self.mode == 0 else None if self.mode == 1 else None
        except Exception as error:
            print(error)
            self.mode = 0


class StatusBar(QtWidgets.QStatusBar):
    Size = 40, 40
    Ratio = 26.0

    def __init__(self, parent):
        super().__init__(parent)

        self.refresh = ReloadButton(self, str(Misc.Gifs / "searching.gif"))

        self.git = ClickLabel(self)
        self.stay_safe = QtWidgets.QLabel(self)
        self.force_update = QtWidgets.QAction(self)

        self.threads = QtWidgets.QLCDNumber(self)
        self.process = QtWidgets.QLCDNumber(self)

        self.searching = None
        self.working = threading.Lock()
        self.thread_safe, self.process_safe = threading.Lock(), threading.Lock()

        self.arrange()

    def arrange(self):
        self.addPermanentWidget(self.refresh)
        self.addPermanentWidget(self.git)
        self.addPermanentWidget(self.stay_safe)
        self._arrange_counts()

        self.setSizeGripEnabled(False)

        self.git.clicked.connect(lambda x=True: webbrowser.open("https://github.com/RahulARanger/Rash"))

        resized = QtGui.QPixmap(str(Misc.Icons / "stay_safe.png"))
        resized.setDevicePixelRatio(StatusBar.Ratio)

        self.stay_safe.setPixmap(resized)
        self.stay_safe.setToolTip("Stay Safe")
        self.stay_safe.setStatusTip("Stay Safe and wear mask")

        self.refresh.setToolTip("Checks for update!")
        self.git.setStatusTip("Redirect to https://github.com/RahulARanger/Rash")
        self.git.setToolTip("Redirects to Github Page")
        self.git.load_gif(str(Misc.Gifs / "github.gif"), 20)

        self._arrange_counts()

    def _arrange_counts(self):
        RashThreadManager.register_submit(self.register_thread_count)
        RashThreadManager.register_done(self.finished_thread_count)

        self.threads.display(
            len(threading.enumerate()) - 1
        )

        self.threads.setToolTip("Number of Running Threads")
        self.threads.setStatusTip("No. of Threads running background")

        self.addPermanentWidget(self.threads)

    def register_thread_count(self):
        with self.thread_safe:
            self.threads.display(self.threads.value() + 1)

    def register_process_count(self):
        pass

    def finished_thread_count(self, _):
        with self.thread_safe:
            self.threads.display(self.threads.value() - 1)

    def finished_process_count(self):
        pass


class TextBrowser(QtWidgets.QTextBrowser):
    Entered = QtCore.Signal(QtCore.QEvent)
    Redirected = QtCore.Signal(QtCore.QUrl)

    def __init__(self, parent):
        super().__init__(parent)
        self.setOpenLinks(False)

        self.anchorClicked.connect(self.redirect)

    def enterEvent(self, event):
        self.Entered.emit(event)
        return super().enterEvent(event)

    def redirect(self, url: QtCore.QUrl):
        check = url.toString()
        return self.Redirected.emit(check[1:]) if check.startswith("#") else self.setSource(url)


class GifHandler(QtGui.QMovie):
    def __init__(self, parent, filename, ratio):
        super().__init__(str(filename))

        self.setParent(parent)
        self.ratio = ratio
        self.frameChanged.connect(self._maintain)

    def _maintain(self):
        pixmap = self.currentPixmap()
        self.parent().setPixmap(pixmap.scaled(pixmap.size() / self.ratio, QtCore.Qt.KeepAspectRatio))


class GifButton(QtWidgets.QLabel):
    Clicked = QtCore.Signal(str)

    def __init__(self, parent, gif, timeout=None):
        super().__init__(parent)
        self.safety = threading.Lock()
        self.timeout = timeout

        self.setMovie(QtGui.QMovie(str(gif)))

        self.arrange()

    def arrange(self):
        pass

    def stop_there(self):
        pass

    def mousePressEvent(self, event):
        self.lock_it()

        return super().mousePressEvent(event)

    def enterEvent(self, event):
        self.start_gif()

        return super().enterEvent(event)

    def leaveEvent(self, event):

        return super().leaveEvent(event)

    def start_gif(self):
        if self.safety.locked():
            return

        self.movie().start()

    def stop_gif(self):
        if self.safety.locked():
            return

        self.movie().stop()

    def lock_it(self):
        if self.safety.locked():
            return

        self.safety.acquire() if self.timeout else self.safety.acquire(timeout=self.timeout)

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        self.Clicked.emit()

    def unlock_it(self):
        if not self.safety.locked():
            return

        QtWidgets.QApplication.restoreOverrideCursor()
        self.safety.release()
