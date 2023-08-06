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

if has_tinydb_dependencies_for_sacred:
    from digitallab.helper.database_interface import TinyDBInterface

if has_pymongo:
    from digitallab.helper.database_interface import MongoDBInterface

from digitallab.helper.singleton import Singleton
from digitallab.helper.storage import DatabaseConnectInformation


@Singleton
class DBAccess:
    def connect(self, database_connect_information: DatabaseConnectInformation,
                cache_id: str = "default"):
        assert database_connect_information.has_connection()
        if hasattr(self, "databases"):
            for database in self.databases:
                database.close_connection()
        self.databases = []
        if database_connect_information.has_tinydb_connection():
            if has_tinydb_dependencies_for_sacred:
                self.databases.append(TinyDBInterface(database_connect_information.tinydb_path))
            else:
                raise_depencies_for_tinydb_missing_error()
        if database_connect_information.has_mongodb_connection():
            if has_pymongo:
                self.databases.append(
                    MongoDBInterface(database_connect_information.mongodb_url, database_connect_information.mongodb_db,
                                     collection_name=database_connect_information.mongodb_collection))
            else:
                raise_pymongo_missing_error()

        if not hasattr(self, "keys"):
            self.keys = {"result": 1, "config": 1}

        self.is_connected = True
        self.cache_id = cache_id

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
        if hasattr(self, "is_connected"):
            if self.is_connected:
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

                cache = Cache(self.cache_id, min_stop_time, self.keys)

                if cache.cache is None:
                    all_docs = most_recent_database.find({"status": "COMPLETED"})
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
        raise ConnectionError("Please connect to database first.")
