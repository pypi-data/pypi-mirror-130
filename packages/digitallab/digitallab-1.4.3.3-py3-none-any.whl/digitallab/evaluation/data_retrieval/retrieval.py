#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import json
from functools import partial
from multiprocessing import Pool
from typing import Union
import pandas as pd

from digitallab.evaluation.data_retrieval.cache import Cache
from digitallab.evaluation.helper.flatten import flatten_dict
from digitallab.helper.storage import DatabaseConnectInformation
from digitallab.helper.optionals import OptionalImports

optional_imports = OptionalImports()

if optional_imports.tinydb_can_be_used():
    from digitallab.helper.database_interface import TinyDBInterface

if optional_imports.mongodb_can_be_used():
    from digitallab.helper.database_interface import MongoDBInterface


class DataRetrieval:
    def __init__(self, experiment_name: str, version: str, database_connect_information: DatabaseConnectInformation,
                 retrieve_keys_json_path_or_dict=None,
                 cache_id: Union[str, None] = None, force_use_of_cache: bool = False):
        self.databases = []
        if database_connect_information.has_tinydb_connection():
            if optional_imports.tinydb_can_be_used():
                self.databases.append(TinyDBInterface(database_connect_information.tinydb_path))
            else:
                optional_imports.raise_depencies_for_tinydb_missing_error()
        if database_connect_information.has_mongodb_connection():
            if optional_imports.mongodb_can_be_used():
                self.databases.append(
                    MongoDBInterface(database_connect_information.mongodb_url, database_connect_information.mongodb_db,
                                     collection_name=database_connect_information.mongodb_collection))
            else:
                optional_imports.raise_pymongo_missing_error()

        if retrieve_keys_json_path_or_dict is None:
            self.keys = {"result": 1, "config": 1}
        else:
            self.set_retrieve_keys(retrieve_keys_json_path_or_dict)

        self.cache_id = experiment_name if cache_id is None else cache_id
        self.experiment_name = experiment_name
        self.experiment_version = version
        self.force_use_of_cache = force_use_of_cache

    def set_retrieve_keys(self, keys_json_path_or_dict: Union[str, dict, None]):
        if keys_json_path_or_dict is None:
            keys_json_path_or_dict = {"result": 1, "config": 1}
        if isinstance(keys_json_path_or_dict, str):
            with open(keys_json_path_or_dict) as json_file:
                self.keys = json.load(json_file)
        elif isinstance(keys_json_path_or_dict, dict):
            self.keys = keys_json_path_or_dict
        else:
            raise TypeError("Argument must be either a string or a dictonary.")

    def get_dataframe(self):
        for database in self.databases:
            database.open_connection()
        min_stop_time = None
        most_recent_database = None
        for database in self.databases:
            stop_time = database.time_stamp_of_most_recent_document()
            if min_stop_time is None:
                min_stop_time = stop_time
                most_recent_database = database
            elif stop_time < min_stop_time:
                min_stop_time = stop_time
                most_recent_database = database

        cache = Cache(self.experiment_name, self.experiment_version, min_stop_time, self.keys, self.cache_id,
                      force_loading_cache=self.force_use_of_cache)

        if cache.cache is None:
            all_docs = most_recent_database.find({"status": "COMPLETED", "config.experiment": self.experiment_name,
                                                  "config.version": self.experiment_version})
            with Pool(8) as pool:
                flatten_docs = pool.map(
                    partial(flatten_dict, keys=self.keys),
                    all_docs)
            df = pd.DataFrame(flatten_docs)
            cache.save_cache(df)
        else:
            df = cache.cache

        for database in self.databases:
            database.close_connection()

        return df
