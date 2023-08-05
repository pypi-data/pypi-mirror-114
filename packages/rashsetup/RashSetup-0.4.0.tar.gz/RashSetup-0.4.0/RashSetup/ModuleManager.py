import sqlite3
import pathlib
import shutil


class ModulePathManager:
    def __init__(self):
        self.mod = pathlib.Path(__file__).parent / "__RashModules__"
        self.mod.mkdir(exist_ok=True)

    def check_module(self, name):
        return (self.mod / name).exists()

    def uninstall_module(self, name):
        shutil.rmtree(self.mod / name)

    def gen_path(self, name):
        mod = self.mod / name
        mod.mkdir(exist_ok=True)
        return str(self.mod / name)

    def _inquiry(self, module, search):
        result = ""
        exception = "No Module Named %s is Found".format(module)
        failed = True

        if not self.check_module(module):
            return result, failed, exception

        entity = self.mod / module / search

        failed = False if entity.exists() else failed
        result = result if failed else str(entity)

        return result, failed, exception

    def inquiry(self, module):
        return self._inquiry(module, "settings.json")

    def fetch_readme(self, module):
        return self._inquiry(module, "README.md")


class DBManager(ModulePathManager):
    def __init__(self):
        super().__init__()
        self.sql = self.mod.parent / "__RashSQL__.sql"
        self.connector = sqlite3.connect(self.mod / "__RashModules__.db", check_same_thread=False)

        self.__start()

    def cursor(self):
        return self.connector.cursor()

    def __start(self):
        temp = self.cursor()
        temp.executescript(self.sql.read_text())
        self.connector.commit()

    def sql_code(self, code, *args):
        return self.execute_one_line(
            *self.execute_one_line(
                "SELECT SQL, Empty FROM Sql WHERE Hash = ?", False, code
            ), *args
        )

    def execute_one_line(self, script, all_=False, *args):
        temp = self.cursor()
        temp.execute(script, args)

        return temp.fetchall() if all_ else temp.fetchone()

    def commit(self):
        self.connector.commit()

    def close(self):
        self.connector.close()
