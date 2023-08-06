#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import pkg_resources


class OptionalImports:
    def __init__(self):
        self.has_hashfs = False
        self.has_tinydb_serialization = False
        self.has_tinydb = False
        self.has_pymongo = False
        self.__inspect_optional_imports()

    def __inspect_optional_imports(self):
        self.__inspect_pymongo()
        self.__inspect_tinydb()
        self.__inspect_tinydb_serialization()
        self.__inspect_hashfs()

    def __inspect_pymongo(self):
        try:
            import pymongo
            from pymongo import MongoClient

            self.has_pymongo = True
        except:
            self.has_pymongo = False

    def __inspect_tinydb(self):
        try:
            pkg_resources.require("tinydb~=3.15.2")
            import tinydb

            self.has_tinydb = True
        except:
            self.has_tinydb = False

    def __inspect_tinydb_serialization(self):
        try:
            pkg_resources.require("tinydb-serialization~=1.0.4")
            import tinydb_serialization

            self.has_tinydb_serialization = True
        except:
            self.has_tinydb_serialization = False

    def __inspect_hashfs(self):
        try:
            pkg_resources.require("hashfs")
            import hashfs

            self.has_hashfs = True
        except:
            self.has_hashfs = False

    def mongodb_can_be_used(self):
        return self.has_pymongo

    def tinydb_can_be_used(self):
        return self.has_tinydb and self.has_tinydb_serialization and self.has_hashfs

    def raise_depencies_for_tinydb_missing_error(self):
        if not self.has_tinydb:
            raise ImportError(
                "tinydb~=3.15.2 not found. Please note that tinydb>=4.0.0 is not supported by sacred right now.")
        elif not self.has_tinydb_serialization:
            raise ImportError(
                "tinydb-serialization~=1.0.4 not found. Please note that tinydb-serialization>=2.0.0 is not supported "
                "by sacred right now.")
        elif not self.has_hashfs:
            raise ImportError("hashfs not found.")

    def raise_pymongo_missing_error(self):
        raise ImportError("pymongo not found.")
