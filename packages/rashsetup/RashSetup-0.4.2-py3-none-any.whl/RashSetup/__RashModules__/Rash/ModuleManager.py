from .Modules import *
import webbrowser
import threading
import multiprocessing
from PySide2.QtWebEngineWidgets import QWebEngineView


class Engine(QWebEngineView):
    def __init__(self, parent):
        super().__init__(parent)

    def load_loading(self):
        self.load(
            QtCore.QUrl.fromLocalFile(str(
                Misc.Misc / "HTML" / "loading_readme.html")
            )
        )

    def load_raw(self, html):
        self.setHtml(
            html, QtCore.QUrl.fromLocalFile(str(Misc.Misc.parent))
        )


class Home(QtWidgets.QWidget):
    StartEngine = QtCore.Signal()  # starts the engine
    CloseEngine = QtCore.Signal()  # closes engine

    ShowModule = QtCore.Signal(str)  # pipes raw HTML from DB

    PipeRaw = QtCore.Signal(str)  # pipes HTML from Home to Engine
    Load = QtCore.Signal()  # makes Engine to view loading.html
    Refresh = QtCore.Signal()  # refreshes Engine

    ShowTemp = QtCore.Signal(QtWidgets.QWidget)
    LoadTemp = QtCore.Signal(str)

    EmitProcess = QtCore.Signal(logging.Logger, LogHandler)

    def __init__(self, parent):
        super().__init__(parent)
        self.setLayout(
            QtWidgets.QVBoxLayout()
        )

        self.engine = None
        self.temp = None
        self.displayed = True

        self.connect_signals()
        self.prev = "Rash"

        self.StartEngine.emit()

    def reload(self, url, is_file):
        pass

    def connect_signals(self):
        self.StartEngine.connect(self._setup)
        self.CloseEngine.connect(self._clean)
        self.ShowModule.connect(self.load_module)

    @QtCore.Slot()
    def _setup(self):
        if self.engine:
            return

        self.engine = Engine(self)
        self.layout().addWidget(self.engine)

        RashLogger.debug("Starting WebEngineView")

        self.PipeRaw.connect(self.engine.load_raw)
        self.Load.connect(self.engine.load_loading)
        self.retrace()

    def _grab(self, raw):
        self.setFocus()

    @QtCore.Slot()
    def _clean(self):
        RashLogger.info("Closing WebEngineView")

        # DISCONNECTING SIGNALS
        self.PipeRaw.disconnect(self.engine.load_raw)
        self.Load.disconnect(self.engine.load_loading)

        # DELETING ENGINE
        self.layout().removeWidget(self.engine)
        self.engine.deleteLater()
        self.engine = None

    @QtCore.Slot(str)
    def load_module(self, module):
        self.StartEngine.emit()  # starts the engine

        result, failed, why = RashDB.fetch_readme(module)

        if not failed:
            return self.PipeRaw.emit(result.read_text())

        # show why it's failed

    def retrace(self):
        return self.ShowModule.emit(self.prev)


class PluginHandler(QtWidgets.QFrame):
    Update = QtCore.Signal()
    Lock = QtCore.Signal(int, bool)

    Trigger = QtCore.Signal()
    Display = QtCore.Signal(pathlib.Path)
    EmitProcess = QtCore.Signal(logging.Logger, LogHandler)

    PipeRaw = QtCore.Signal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.safety = threading.Lock()

        self.search = QtWidgets.QLineEdit(self)
        self.search_it = QtWidgets.QAction(self.search)

        self.tab_view = QtWidgets.QTabWidget(self)

        self.downloaded = ShowPluginArea(self.tab_view)
        self.install = InstallPluginArea(self.tab_view)

        self.tab_view.addTab(self.downloaded, "Installed")
        self.tab_view.addTab(self.install, "Search")

        self.arrange()
        self.connect_signals()

    def arrange(self):
        self.setLayout(QtWidgets.QVBoxLayout())

        self.search.setClearButtonEnabled(True)
        self.search.addAction(self.search_it, QtWidgets.QLineEdit.TrailingPosition)
        self.search_it.setIcon(QtGui.QIcon(str(Misc.Icons / "search.png")))

        self.layout().addWidget(self.search)
        self.layout().addWidget(self.tab_view)

    def connect_signals(self):
        self.tab_view.currentChanged.connect(
            self.rearrange
        )

        self.search_it.triggered.connect(self.search_them)
        self.search.textChanged.connect(self.save_cache)
        self.search.returnPressed.connect(self.search_it.trigger)
        self.Lock.connect(self.lock_search)

        self.install.display.EmitProcess.connect(self.EmitProcess)
        self.install.display.PipeRaw.connect(self.PipeRaw)

        for tab in (self.install, self.downloaded):
            tab.Busy.connect(self.Lock)

    def rearrange(self):
        current: ShopTab = self.tab_view.currentWidget()

        self.search.setText(current.cache)
        self.Lock.emit(self.tab_view.indexOf(current), not current.locked())

    def save_cache(self):
        current: ShopTab = self.tab_view.currentWidget()
        return current.update_cache(self.search.text())

    def search_them(self):
        current: ShopTab = self.tab_view.currentWidget()
        current.search(self.search.text())

    def free(self):
        self.search_it.setDisabled(False)

    def register_process(self):
        with self.safety:
            self.count.display(self.count.value() + 1)

    def register_started(self):
        with self.safety:
            self.count.display(self.count.value() - 1)

    def lock_search(self, from_, lie=False):
        current = self.tab_view.currentWidget()

        if self.tab_view.indexOf(current) != from_:
            return

        self.search.setDisabled(not lie)
        self.search_it.setDisabled(not lie)


class ShopTab:
    def __init__(self):
        self.cache = ""
        self.working = False

    def update_cache(self, text):
        self.cache = text

    def search(self, text):
        return text

    def locked(self):
        return self.working

    def kill(self):
        pass

    def lock(self):
        pass


class QueryItem(QtWidgets.QWidget):
    def __init__(self, parent, id_):
        super().__init__(parent)
        self._id = id_

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)  # bring it to left

    def text(self):
        return self._id


class InstallPluginArea(
    QtWidgets.QSplitter,
    ShopTab
):
    Busy = QtCore.Signal(int, bool)
    Install = QtCore.Signal(str, dict)

    def __init__(self, parent):
        super().__init__(parent)
        ShopTab.__init__(self)

        self.setOrientation(QtCore.Qt.Vertical)

        self.display = DisplaySearch(
            self
        )

        self.tasks = QtWidgets.QListWidget(
            self
        )

        self.addWidget(self.display)
        self.addWidget(self.tasks)

    def search(self, text):
        if text == "":
            return

        return RashThreadManager.submit(
            self.__search, text
        )

    def __search(self, url):
        self.working = True
        self.Busy.emit(1, False)

        try:
            self.display.search(url)
        except Exception as _:
            RashLogger.exception(
                "Failed to Search for %s".format(url), exc_info=True
            )

        self.working = False
        self.Busy.emit(1, True)


class DisplaySearch(
    QtWidgets.QTextBrowser
):
    Result = QtCore.Signal(bool, dict, str)
    PipeRaw = QtCore.Signal(str)

    EmitProcess = QtCore.Signal(logging.Logger, LogHandler)

    def __init__(self, parent):
        super().__init__(parent)
        self.loaded = []
        self.connect_signals()
        self.setOpenExternalLinks(True)

    def connect_signals(self):
        self.Result.connect(self.show_result)
        self.anchorClicked.connect(self.redirect)

    def search(self, module):
        cached = RashDB.sql_code(3, module)
        temp = RashDB.sql_code(2, module)

        if cached or temp:
            return

        handler = LogHandler()
        process = RashProcess(
            ModuleCheckerSetup, module, handler=handler
        )

        self.loaded.clear()
        self.loaded.append(handler)
        self.loaded.append(process)

        self.EmitProcess.emit(multiprocessing.get_logger(), handler)
        #
        process.start()
        process.join(6)

        raw, status, why = process.results()

        return self.Result.emit(status, raw if status else why, module)

    def show_result(self, found, raw, url):
        html = (
                Misc.Misc / "HTML" / ("ModuleFound.html" if found else "NotFound.html")
        ).read_text()

        print(raw)

        self.setHtml(
            html.format(
                os.path.split(url)[-1], *(
                    raw["setup.py"], raw["settings.json"]
                ) if found else (
                    raw
                )
            )
        )

    def redirect(self, url: QtCore.QUrl):
        mode = os.path.split(url.toString())[-1]

        if mode == "#install":
            pass

        elif mode == "#preview":
            self.PipeRaw(self.loaded[3]) if self.loaded else None

        elif mode == "#provoke":
            return getattr(self.loaded[0], "__switch")() if self.loaded else None

    def emit_raw(self):
        if not self.loaded.get("failed", True):
            return self.PipeRaw.emit(self.loaded["result"])

        self.loaded["exception"] = self.loaded.get(
            "exception", "Proper Results were not returned"
        )

        return self.PipeRaw.emit(
            (Misc.Misc / "HTML" / "NotFound.html").read_text().format(
                self.loaded["exception"]
            )
        )

    def reset(self):
        self.setHtml(
            (
                    Misc.Misc / 'HTML' / "Intro.html"
            ).read_text()
        )


class DownloadingItem(QueryItem):
    def __init__(
            self,
            parent,
            id_,
            name,
            process
    ):
        super().__init__(parent, id_)

        self.process = process

        self.name = QtWidgets.QLabel(self)
        self.name.setText(name)

        self.kill = QtWidgets.QToolButton(self)
        self.kill.setIcon(
            QtGui.QIcon(
                str(Misc.Gifs / "kill.svg")
            )
        )

        self.layout().addWidget(self.name)
        self.layout().addWidget(self.kill)


class PluginShow(QueryItem):
    def __init__(self, parent, name, url, version):
        super().__init__(parent, name)

        self.name = QtWidgets.QLabel(self)
        self.reload = QtWidgets.QLabel(self)
        self.uninstall = QtWidgets.QLabel(self)

        self.layout().addWidget(self.name)
        self.layout().addWidget(self.reload)
        self.layout().addWidget(self.uninstall)

        self.uninstall.setVisible(name != "Rash")

        self.name.setText(name)
        self.reload.setToolTip(version)
        self.reload.setStatusTip(f"Current Version for {name} is {version}")
        self.reload.setText("reloading")
        self.uninstall.setText("Uninstall")

    def key(self):
        return self.name.text()


class ShowPluginArea(
    QtWidgets.QListWidget,
    ShopTab
):
    Busy = QtCore.Signal(int, bool)
    PipeRaw = QtCore.Signal(str)
    Refresh = QtCore.Signal(str)
    Add = QtCore.Signal(str, str, str)

    Hide = QtCore.Signal(QtWidgets.QListWidgetItem, bool)

    def __init__(self, parent):
        super().__init__(parent)
        ShopTab.__init__(self)

        self._cache = set()
        self._setup()
        self.connect_signals()

    def connect_signals(self):
        self.Add.connect(self._add)
        self.Hide.connect(self.setItemHidden)

    def _setup(self):
        RashThreadManager.submit(
            self._load
        )

    def _load(self):
        items = RashDB.sql_code(1)

        for item in items:
            self.Add.emit(*item)

    def _add(self, name, url, version):
        temp = QtWidgets.QListWidgetItem(self)
        self.setItemWidget(temp, PluginShow(self, name, url, version))

    def search(self, text):
        return RashThreadManager.submit(
            self._search, text.lower()
        )

    def _search(self, text):
        for item in tuple(self._cache) + tuple(range(self.count())):
            item = self.item(item) if type(item) == int else item
            result = text not in self.itemWidget(item).key().lower()

            self.Hide.emit(item, result)

            self._cache.add(item) if result else self._cache.remove(item)

    def refresh(self):
        self._setup()
