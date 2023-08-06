from digitallab.helper.optionals import OptionalImports
from digitallab.helper.singleton import Singleton

optional_imports = OptionalImports()

if optional_imports.tinydb_can_be_used():
    from tinydb import TinyDB

if optional_imports.tinydb_can_be_used():
    @Singleton
    class TinyDBAccessRegister:
        def open_connection(self, path_to_dir):
            if not hasattr(self, "connected_objects"):
                self.__setup()

            if self.connected_objects > 0:
                self.connected_objects += 1
                return self.db
            else:
                self.db = TinyDB(path_to_dir + "/metadata.json")
                self.connected_objects += 1
                return self.db

        def close_connection(self):
            if not hasattr(self, "connected_objects") or self.connected_objects == 0:
                raise ValueError("'open_connection' was not called beforehand.")
            self.connected_objects -= 1
            if self.connected_objects == 0:
                self.db.close()

        def __setup(self):
            self.connected_objects = 0
            self.db = None
