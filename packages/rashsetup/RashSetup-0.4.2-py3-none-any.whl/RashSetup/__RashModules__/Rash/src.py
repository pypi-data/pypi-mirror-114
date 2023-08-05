import concurrent.futures
import multiprocessing
import pathlib
import gc
import urllib.request
import logging
import queue

from typing import Tuple, Optional, Any, Callable
from RashSetup.internal import *


__all__ = [
    # module based
    "pathlib",
    "gc",

    # classes
    "Downloader",

    # objects
    "RashLogger",
    "RashThreadManager",
    "RashDB",
    "LAUNCHER",
    "SIGNALS"
]

# RashSetup bases
__all__.extend([
    # classes
    "JsonHandler",
    "TempHandler",
    "LockOut",
    "LockErr",
    "SettingsParser",
    "ProcessListener"
])


class Downloader:
    def __init__(self, path, urls):
        self.p_callback, self.f_callback = None, None

        self.to_do = urls
        self.goal = path

        self.maintain = queue.Queue()

    def register_progress_callback(self, callback):
        self.p_callback = callback

    def register_finished_callback(self, callback):
        self.f_callback = callback

    def initiate(self):
        started = False  # to indicate whether this is dng some work or nt

        for _ in self.to_do:
            self.maintain.put(False)  # job not done

        for url in self.to_do:
            entity = self.goal / url

            if entity.exists():
                self.maintain.get()  # job already done
                self.f_callback() if self.maintain.qsize() == 0 and not started else None

                continue

            started = False  # yes it's dng some work

            future = RashThreadManager.submit(
                self.download, url, entity
            )

            future.add_done_callback(
                self.update
            )

        return started

    def download(self, url, entity):
        try:
            local_file, headers = urllib.request.urlretrieve(
                self.to_do[url], entity
            )
            return True, str(local_file)
        except Exception as error:
            return False, error

    def update(self, future):
        self.maintain.get()
        self.p_callback(future) if self.p_callback else None

        return None if self.maintain.qsize() != 0 else self.f_callback() if self.f_callback else None


class RashModuleManager(ModuleManager):
    def __init__(self):
        super().__init__()


class CallBackExecutor:
    def __init__(self):
        self._callbacks: list = [None, None]

    def register_submit(self, callback: Callable):
        self._callbacks[0] = callback

    def register_done(self, callback):
        self._callbacks[1] = callback

    def submit(self, *args):
        return self._callbacks[0]() if self._callbacks[0] else None


class ThreadPoolExecutor(concurrent.futures.ThreadPoolExecutor, CallBackExecutor):

    def __init__(
            self,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        CallBackExecutor.__init__(self)

    def submit(self, func, *args, **kwargs):
        future = super().submit(func, *args, **kwargs)
        CallBackExecutor.submit(self)

        future.add_done_callback(self._callbacks[1]) if self._callbacks[1] else None

        return future


class ProcessPoolExecutor(CallBackExecutor):
    def __init__(self, prefix=""):
        super().__init__()
        self.prefix = prefix
        self.collect = set()

    def bg(self, process: multiprocessing.Process):
        process.start()

        process.name = (process.name if process.name else "") + self.prefix
        self._callbacks[0]() if self._callbacks[0] else None
        self.collect.add(process)

    def submit(self, process: multiprocessing.Process, timeout=None):
        self.bg(process)

        process.join(timeout)
        super().submit()

        return self.close(process)

    def close(self, process: multiprocessing.Process):
        self.collect.remove(process)
        process.close()


# setting the Threading Manager
RashThreadManager = ThreadPoolExecutor(None, "Rash")
RashProcessManager = ProcessPoolExecutor("Rash")

LAUNCHER = Launcher(__file__, RashThreadManager)

# setting logger

RashLogger = logging.getLogger()
RashLogger.setLevel(logging.DEBUG)

# Setting DB
RashDB = RashModuleManager()

SIGNALS = {}
