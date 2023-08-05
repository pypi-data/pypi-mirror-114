from .Docks import *
import sys

__all__ = [
    "Start"
]


def change_channel(caller):
    for _ in getattr(caller, "__channel"):
        _()


def register_channel(channel, *actions):
    setattr(channel, "__channel", actions)


class RashSplash(QtWidgets.QSplashScreen):
    set_info = QtCore.Signal(str)
    finished = QtCore.Signal(object)

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint
        )

        self.p_bar = QtWidgets.QProgressBar(self)
        self.inform = QtWidgets.QLabel(self)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft)

        self.layout().addWidget(self.p_bar)
        self.layout().addWidget(self.inform)

        self.failed = ""

        self.set_info.connect(self.inform.setText)

    def process(self):
        handler = JsonHandler(Misc.Settings)
        parsed = handler.load()["downloads"]
        length = len(parsed)

        started = True
        self.p_bar.setRange(0, 0)

        for index, directory in enumerate(parsed):
            path = Misc.Misc / directory
            None if path.exists() else path.mkdir()

            ware = Downloader(path, parsed[directory])

            ware.register_progress_callback(self.update_process)
            ware.register_finished_callback(
                lambda: self.done(index + 1 == length)
            )

            started = all(
                (started, ware.initiate())
            )

        self.done(True) if started else None  # to avoid race condition

    def done(self, fully):
        return self.finished.emit(self.failed) if fully else self.p_bar.setValue(0)

    def update_process(self, future):
        status, info = future.result()

        if status:
            return self.set_info.emit("Downloading " + info)

        self.set_info.emit("Failed to Download some files")
        self.failed = info


class RashMain(QtWidgets.QMainWindow):
    PluginClicked = QtCore.Signal(str)

    def __init__(self):
        super().__init__()

        self.central = QtWidgets.QFrame(self)
        self.docks = DockWidget(self)
        self.status = StatusBar(self)
        self.tool_bar = QtWidgets.QToolBar(self)

        self.home = Home(self)
        self.logger = LogWindow(self.central)

        self.stack_pages = QtWidgets.QStackedLayout()

        self.plugin = PluginHandler(
            self.docks.project_frame
        )

        self.arrange()
        self.arrange_misc()
        self.arrange_window()
        self.connect_signals()

        RashLogger.info(
            "Started Rash"
        )

    # noinspection PyBroadException
    def arrange(self):
        Misc.ensure_paths()
        self.setMinimumSize(QtCore.QSize(600, 300))
        self.setStyleSheet(
            (Misc.Misc / "CSS" / "dark_theme.css").read_text()
        )
        self.setCentralWidget(self.central)
        self.central.setLayout(self.stack_pages)
        self.stack_pages.addWidget(self.home)

        self.home.setObjectName("Browser")

    def arrange_misc(self):
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.docks)

        self.setStatusBar(self.status)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.tool_bar)

        # --- HOME
        home = QtWidgets.QToolButton(self.tool_bar)
        home.setIcon(QtGui.QIcon(str(Misc.Icons / "house.png")))
        self.tool_bar.addWidget(home)

        self.register_both(home, self.home, self.plugin, home.clicked, "Shop")

        # --- WORKSPACE
        workspace = QtWidgets.QToolButton(self.tool_bar)
        workspace.setIcon(QtGui.QIcon(str(Misc.Icons / "workspace.png")))

        self.tool_bar.addWidget(workspace)

        self.register_dock_channel(workspace, self.docks.tree, workspace.clicked, "Workspace")

        # --- Logs
        logs = QtWidgets.QToolButton(self.tool_bar)
        logs.setIcon(QtGui.QIcon(str(Misc.Icons / "logs.png")))
        self.register_window(logs, self.logger, logs.clicked)

        self.tool_bar.addWidget(logs)

        # --- Home

        self.register_window(
            self.plugin, self.home, self.plugin.Display
        )

        home.click()

    def arrange_window(self):
        self.setWindowTitle("Rash")
        self.setWindowIcon(QtGui.QIcon(str(Misc.Icons / "rash.ico")))

    def register_dock_channel(self, caller, channel, signal, title):
        self.docks.stacked.addWidget(channel)

        register_channel(
            caller,
            lambda: self.docks.stacked.setCurrentWidget(channel),
            lambda: self.docks.title.setText(title)
        )

        signal.connect(
            lambda: change_channel(caller)
        ) if signal else None

    def register_both(self, caller, main_channel, dock_channel, signal, title):
        self.stack_pages.addWidget(main_channel)
        self.docks.stacked.addWidget(dock_channel)

        register_channel(
            caller,
            lambda: self.stack_pages.setCurrentWidget(main_channel),
            lambda: self.docks.stacked.setCurrentWidget(dock_channel),
            lambda: self.docks.title.setText(title)
        )

        signal.connect(
            lambda: change_channel(caller)
        ) if signal else None

    def register_window(self, caller, channel, signal):
        self.stack_pages.addWidget(channel)

        register_channel(
            caller,
            lambda: self.stack_pages.setCurrentWidget(channel)
        )

        signal.connect(
            lambda: change_channel(caller)
        ) if signal else None

    def register_workspace(self, caller, channel, signal):
        pass

    def connect_signals(self):
        # self.plugin.Display.connect(self.home.ShowRaw)
        self.stack_pages.currentChanged.connect(self.notify)

        self.home.EmitProcess.connect(self.logger.AddProcess)
        self.plugin.EmitProcess.connect(self.logger.AddProcess)
        self.plugin.PipeRaw.connect(self.showHtml)

    def notify(self):
        RashThreadManager.submit(
            self.home.StartEngine.emit if self.stack_pages.currentWidget() == self.home else self.home.CloseEngine.emit
        )

    def showHtml(self, raw):
        self.stack_pages.setCurrentWidget(self.home)
        self.home.PipeRaw.emit(raw)

    def close(self):
        LAUNCHER.close()
        RashThreadManager.shutdown()

        return super().close()


class Start:
    def __init__(self):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

        self.initiate = QtWidgets.QApplication(sys.argv)

        self.rash = None
        self.splash = RashSplash()

        self.splash.finished.connect(self.start_rash)

        self.splash.show()
        self.splash.process()

        sys.exit(
            self.initiate.exec_()
        )

    def start_rash(self, failed):
        if failed:
            return self.trigger_warning(failed)

        self.rash = RashMain()

        self.splash.finish(self.rash)

        self.rash.show()

        self.rash.adjustSize()

        self.initiate.lastWindowClosed.connect(
            self.close_rash
        )

    def close_rash(self):
        self.rash.close()

    def trigger_warning(self, failed):
        box = QtWidgets.QMessageBox()

        box.setWindowTitle("Error Downloading Files")
        box.setText("<h1>Faced an Exception while downloading core files</h1>")

        info, detail = FormatException(failed)

        box.setInformativeText(
            info
        )

        box.setDetailedText(
            detail
        )

        button = box.addButton(
            "Copy to Clipboard", QtWidgets.QMessageBox.HelpRole
        )

        button.setText("Copy to Clipboard")
        button.clicked.connect(lambda: FormatException(failed, True))

        box.setWindowIcon(QtGui.QIcon(str(Misc.Icons / "rash.ico")))

        self.splash.finish(box)
        box.exec_()
        self.safe_close()

    def safe_close(self):
        self.splash.close()

        LAUNCHER.close()
        RashThreadManager.shutdown()

        sys.exit(0)
