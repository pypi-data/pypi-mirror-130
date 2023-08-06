#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from digitallab.helper.database_interface import TinyDBInterface, MongoDBInterface
from digitallab.helper.storage import DatabaseConnectInformation


class ExperimentValidation:
    def __init__(self, database_connect_information: DatabaseConnectInformation,
                 rerun_non_optimal=False):
        assert database_connect_information.has_connection()
        self.rerun_non_optimal = rerun_non_optimal
        self.databases = []
        if database_connect_information.has_tinydb_connection():
            self.databases.append(TinyDBInterface(database_connect_information.tinydb_path))
        if database_connect_information.has_mongodb_connection():
            self.databases.append(
                MongoDBInterface(database_connect_information.mongodb_url, database_connect_information.mongodb_db,
                                 collection_name=database_connect_information.mongodb_collection))

    def open_connection(self):
        for database in self.databases:
            database.open_connection()

    def close_connection(self):
        for database in self.databases:
            database.close_connection()

    def is_experiment_eligible(self, config):
        essential_keys = ("number_of_repetitions", "version")
        for k in essential_keys:
            if k not in config.keys():
                raise KeyError("%s was not found in experiment setting." % k)

        for database in self.databases:
            if database.count_documents({"config.version": config["version"]}) > 0:
                query = dict()
                query2 = dict()
                for key, value in config.items():
                    if key not in ("number_of_repetitions", "time_limit"):
                        query["config." + key] = value
                        query2["config." + key] = value
                query["status"] = "COMPLETED"
                query2["status"] = "RUNNING"
                if self.rerun_non_optimal:
                    query["result.optimal"] = True
                    query2["result.optimal"] = True
                if database.count_documents(query) < 1 and database.count_documents(query2) < 1:
                    return True
            else:
                return True
        return False


def validate_if_experiment_eligible(config, database_connect_information: DatabaseConnectInformation,
                                    rerun_non_optimal=False):
    experiment_query = ExperimentValidation(database_connect_information, rerun_non_optimal=rerun_non_optimal)
    experiment_query.open_connection()
    b = experiment_query.is_experiment_eligible(config)
    experiment_query.close_connection()
    return b


def validate_if_experiments_eligible(configs, database_connect_information: DatabaseConnectInformation,
                                     rerun_non_optimal=False):
    experiment_query = ExperimentValidation(database_connect_information, rerun_non_optimal=rerun_non_optimal)
    bool_list = []
    experiment_query.open_connection()
    for conf in configs:
        bool_list.append(experiment_query.is_experiment_eligible(conf))
    experiment_query.close_connection()
    return bool_list
