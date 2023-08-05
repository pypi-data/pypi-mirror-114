import gc
import multiprocessing
import sys

from .shared import *
from .RashScrappers.RashScrappers.spiders import *
from .ModuleManager import *

import queue
import logging
import importlib
import subprocess

import scrapy.crawler

__all__ = [
              "SettingsParser",
              "ModuleManager",
              "TempHandler"
          ] + ALL


class QueueHandler(logging.handlers.QueueHandler):
    def __init__(self, queue_):
        super().__init__(queue_)

    def handle(self, record):
        # to make this pickleable
        # avoiding all lambda functions from scrapy logs

        modified = logging.LogRecord(
            record.name,
            record.levelno,
            record.pathname,
            record.lineno,
            record.getMessage(),
            args=(),
            exc_info=record.exc_info,
            func=record.funcName,
            sinfo=record.stack_info
        )

        return super().handle(modified)


class Setup:
    def __init__(
            self, pipe=None, log_pipe: queue.Queue = None, url=None, start=False
    ):
        self.pipe = pipe

        self.cache = {
            "failed": True,
            "exception": "Failed before scraping",
            'result': ""
        }

        self._complete(log_pipe) if log_pipe else None

        self.start(url) if start else None

    def _complete(self, pipe):
        self.logger = logging.getLogger("")
        self.logger.addHandler(
            QueueHandler(pipe)
        )

    def start(self, *args):
        pass

    def save(self, _):
        temp = JsonHandler(
            TempHandler()(suffix=".json")
        )

        temp.dump(self.cache)

        self.pipe.saved = temp

        self.logger.info("Saving raw data into %s", temp.file)

        gc.collect()


class DownloadModule(Setup):
    def __init__(self, pipe, log_pipe, url, path):
        super().__init__(pipe, log_pipe, (url, path), True)

    def start(self, abouts):
        crawler = scrapy.crawler.CrawlerProcess(

        )

        future = crawler.crawl(
            RepoSpider, url=abouts[0], pipe=self.cache, path=abouts[1]
        )
        future.addCallback(self.save)

        crawler.start(True)


class SettingsSetup(Setup):
    def __init__(self, save_pipe, log_pipe, url):
        super().__init__(save_pipe, log_pipe, url, True)

    def start(self, url):
        crawler = scrapy.crawler.CrawlerProcess()

        future = crawler.crawl(
            Investigator, url=url, pipe=self.cache
        )

        future.addCallback(
            self.save
        )

        crawler.start(True)


class SettingsParser:
    def __init__(self, json_url):
        self.parsed = json_url if type(json_url) == dict else JsonHandler().parse_url(json_url)

    def name(self):
        return self.parsed["name"]

    def version(self):
        return self.parsed["version"]

    def hosted(self):
        return self.parsed["hosted"]

    def install_required(self):
        temp = TempHandler()(False, ".txt")

        with open(temp, 'w') as writer:
            writer.writelines(self.parsed.get("install_requires", []))

        subprocess.run(
            [
                "pip", "install", '-r', temp
            ]
        )

    def template(self):
        return self.parsed["template"]

    def required(self):
        return self.parsed["install_requires"]


class RawModuleManager(
    DBManager
):
    def __init__(self):
        super().__init__()

        self.linkers = {}

    def _raw_download(self, url, name):
        listen = ProcessListener(
            DownloadModule, url, self.gen_path(name)
        )
        listen.start()

        listen.join()

        return listen.results()

    def download(self, module):
        listen = ProcessListener(
            SettingsSetup, module
        )

        listen.start()

        listen.join()

        result, status, why = listen.results()

        if status:
            result["settings.json"] = SettingsParser(result["settings.json"])

        return result, status, why

    def search_by_url(self, url):
        result = self.sql_code(
            5, url
        )

        return result


class LinkManager(
    RawModuleManager
):
    def __init__(self):
        super().__init__()
        self.linkers = {}

    def activate_link(self, module):
        temp = self.template(module)

        if temp != "Main":
            return False

        self.utils(module)[0]()

        return True

    def register_link(self, asked):
        module = importlib.import_module("." + asked, "RashSetup.__RashModules__")
        result = hasattr(module, "UTILS") and hasattr(module, "TEMPLATE")

        if not result:
            logging.error("Failed to start %s", module)
            return result

        self.linkers[asked] = module
        return True

    def find_link(self, module):
        return self.linkers.get(module, False)

    def template(self, module):
        return getattr(self.linkers[module], "TEMPLATE")

    def utils(self, module):
        return getattr(self.linkers[module], "UTILS")

    def activate_all(self):
        failed = []

        for module in self.sql_code(2):
            logging.info("Starting %s", module)
            result = self.register_link(module)

            if not result:
                failed.append(module)
                continue

            self.activate_link(module)

        return failed


class ModuleManager(
    LinkManager
):
    def __init__(self):
        super().__init__()

    def inquiry(self, module):
        result, failed, exception = super().inquiry(module)
        return None if failed else SettingsParser(result), failed, exception

    def download(self, url):
        result, status, why = super().download(url)
        return self._raw_download(

            url, result["settings.json"].name()

        ) if status else (

            result, status, why

        )

    def investigate(self, module):
        return super().download(module)

    @classmethod
    def Start(cls):
        root = logging.getLogger("")
        root.setLevel(logging.DEBUG)
        root.addHandler(logging.StreamHandler(None))

        temp = ModuleManager()
        _ = "Rash"

        root.info("Checking for the Rash Module")

        result = temp.check_module(_)

        if not result:
            temp.download(
                temp.sql_code(
                    3, _
                )[0]
            )

        skip_code = """
import RashSetup.__RashModules__.Rash
RashSetup.__RashModules__.Rash.Start()    
"""

        return subprocess.Popen(
            [
                sys.executable,
                '-c',
                skip_code
            ],
            creationflags=subprocess.DETACHED_PROCESS
        )
