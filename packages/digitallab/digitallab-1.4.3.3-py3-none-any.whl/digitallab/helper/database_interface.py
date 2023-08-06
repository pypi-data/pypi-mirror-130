import abc
import os

from packaging import version

from digitallab.helper.optionals import OptionalImports

optional_imports = OptionalImports()

if optional_imports.tinydb_can_be_used():
    import tinydb
    from tinydb import Query
    from digitallab.helper.tinydb_access_register import TinyDBAccessRegister

if optional_imports.mongodb_can_be_used():
    from pymongo import MongoClient
    import pymongo


def remove_tree_depth(obj, domain=""):
    ret = {}
    for key, value in obj.items():
        if isinstance(value, dict):
            ret.update(remove_tree_depth(value, domain=domain + key + "."))
        else:
            ret[domain + key] = value
    return ret


# Code and copyright 2021 Ted Brownlow Stack Overflow
# https://stackoverflow.com/questions/57583043/build-search-query-from-a-dict
def predicate(obj, requirements):
    for k, v in requirements.items():
        if k not in obj or obj[k] != v:
            return False
    return True


def dict_to_query(query):
    def query_function(obj):
        return predicate(remove_tree_depth(obj), query)

    if version.parse(tinydb.__version__) > version.parse("4.0.0"):
        return Query().fragment(query)
    else:
        return query_function


class DocumentDataBaseInterface(abc.ABC):
    @abc.abstractmethod
    def open_connection(self):
        pass

    @abc.abstractmethod
    def close_connection(self):
        pass

    @abc.abstractmethod
    def count_documents(self, query):
        pass

    @abc.abstractmethod
    def find(self, query):
        pass

    @abc.abstractmethod
    def time_stamp_of_most_recent_document(self):
        pass


if optional_imports.tinydb_can_be_used():
    class TinyDBInterface(DocumentDataBaseInterface):
        def __init__(self, directory_of_database, collection_name="runs"):
            self.directory_of_database = directory_of_database
            self.db = None
            self.collection_name = collection_name
            self.collection = None

        def open_connection(self):
            # TODO: make sure that there is no trailing backspace
            # TODO: if a long path is given make sure that it exists
            if not os.path.isdir(self.directory_of_database):
                os.mkdir(self.directory_of_database)
            self.db = TinyDBAccessRegister.instance().open_connection(self.directory_of_database)
            self.collection = self.db.table(self.collection_name)

        def close_connection(self):
            TinyDBAccessRegister.instance().close_connection()

        def count_documents(self, query):
            return self.collection.count(dict_to_query(query))

        def find(self, query):
            return self.collection.search(dict_to_query(query))

        def time_stamp_of_most_recent_document(self):
            all_documents = self.collection.all()

            def sort_function(document):
                return document["stop_time"]

            return sorted(all_documents, key=sort_function)[-1]["stop_time"]
else:
    class TinyDBInterface(DocumentDataBaseInterface):
        def __init__(self, directory_of_database, collection_name="runs"):
            pass

        def open_connection(self):
            pass

        def close_connection(self):
            pass

        def count_documents(self, query):
            pass

        def find(self, query):
            pass

        def time_stamp_of_most_recent_document(self):
            pass

if optional_imports.mongodb_can_be_used():
    class MongoDBInterface(DocumentDataBaseInterface):
        def __init__(self, url, database_name, collection_name="runs"):
            self.url = url
            self.database_name = database_name
            self.collection_name = collection_name
            self.db = None
            self.client = None
            self.collection = None

        def open_connection(self, *args):
            self.client = MongoClient(self.url)
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]

        def close_connection(self):
            self.client.close()

        def count_documents(self, query):
            return self.collection.count_documents(query)

        def find(self, query):
            return self.collection.find(query)

        def time_stamp_of_most_recent_document(self):
            return self.collection.find().sort("stop_time", pymongo.DESCENDING).limit(1)[0]["stop_time"]
else:
    class MongoDBInterface(DocumentDataBaseInterface):
        def __init__(self, directory_of_database, collection_name="runs"):
            pass

        def open_connection(self):
            pass

        def close_connection(self):
            pass

        def count_documents(self, query):
            pass

        def find(self, query):
            pass

        def time_stamp_of_most_recent_document(self):
            pass