import os
import json
import urllib.request
from .LAUNCHER import Launcher
import logging.handlers
import multiprocessing
import sys

ALL = [
    "JsonHandler",
    "Launcher",
    "LockOut",
    "LockErr",
    "ProcessListener",
    "ALL"
]

__all__ = ALL


class JsonHandler:
    def __init__(self, file=None):
        self.file = file

    def load(self):
        with open(self.file, 'r') as loaded:
            return json.load(loaded)

    def dump(self, store):
        with open(self.file, 'w') as loaded:
            return json.dump(store, loaded, indent=4)

    def __call__(self, raw: str):
        return json.loads(raw)

    def __str__(self):
        return self.file

    def parse_url(self, raw_link):
        with urllib.request.urlopen(raw_link) as raw:
            return self(raw.read())

    def close(self):
        os.remove(self.file)


class PipeFD:
    def __init__(self, callback=None):
        self.buffer = None
        self.store = None

        self.callback = callback

    def write(self, text):
        return self.callback(text) if self.callback else text

    def writelines(self, lines):
        if not self.callback:
            return lines

        self.callback("".join(lines))

    def fileno(self):
        return self.store.fileno()

    def flush(self):
        return self.store.flush()

    def close(self):
        pass


class LockErr(PipeFD):
    def __init__(self, callback):
        super().__init__(callback)

        self.store = sys.stderr
        self.buffer = sys.stderr.buffer

        sys.stderr = self

    def close(self):
        sys.stderr = self.store


class LockOut(PipeFD):
    def __init__(self, callback):
        super().__init__(callback)

        self.store = sys.stdout
        self.buffer = sys.stdout.buffer

        sys.stdout = self

    def close(self):
        sys.stdout = self.store


class ProcessListener(logging.handlers.QueueListener):
    # TODO: create own Listener to avoid an extra thread

    def __init__(self, target, *args, handler=None):
        self._manager = multiprocessing.Manager()

        self.saved = self._manager.Namespace()
        self.logs = self._manager.Queue()

        self.utils = args[0]

        super().__init__(self.logs, handler if handler else logging.getLogger("").handlers[0])

        self.process = multiprocessing.Process(
            target=target, args=(
                self.saved,
                self.logs,
                *args
            )
        )

    def start(self):
        self.process.start()
        super().start()

    def join(self, timeout=None):
        self.process.join(timeout)

        logging.info("%s[%d] process has finished it's execution", self.process.name, self.process.pid)
        return self.stop()

    def results(self):
        if not hasattr(self.saved, "saved"):
            logging.error(
                "%s[%d] process has failed to return feasible results", self.process.name, self.process.pid
            )

            return False, False, "README Setup failed to grab the README from the %s".format(self.utils)

        print("exit code: ", self.status())

        saved: JsonHandler = self.saved.saved
        loaded = saved.load()
        saved.close()

        if loaded["failed"]:
            logging.error("%s[%d] process has failed due to this exception;", self.process.name, self.process.pid)
            logging.exception(loaded["exception"])
            return False, not loaded["failed"], loaded["exception"]

        return loaded["result"], not loaded["failed"], loaded["exception"]

    def close(self):
        self.process.close()

    def status(self):
        return self.process.exitcode
