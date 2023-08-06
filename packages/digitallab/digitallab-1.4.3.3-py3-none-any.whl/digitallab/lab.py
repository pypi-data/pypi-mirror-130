#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import datetime
import functools
import json
import logging
import random
import traceback
import warnings
from collections import Iterable
from functools import partial
from itertools import compress
from logging.handlers import RotatingFileHandler
# from pathos.multiprocessing import ProcessPool as Pool
from multiprocessing import Pool
from typing import Union

from sacred import Experiment
from sacred.observers import MongoObserver, TinyDbObserver

from digitallab.evaluation.data_processing.all_experiments_database_collector import AllExperimentsDatabaseCollector
from digitallab.evaluation.data_processing.procedural_database_collector import ProceduralDatabaseCollector
from digitallab.evaluation.data_retrieval.retrieval import DataRetrieval
from digitallab.evaluation.plots.box_plot import box_plot_class
from digitallab.evaluation.plots.ecdf_plot import ecdf_plot_class
from digitallab.evaluation.plots.facetoface_density_bar_plot import FaceToFaceDensityBarPlot
from digitallab.evaluation.tables.tables import MeanTable, MedianTable, MinTable, MaxTable
from digitallab.helper.optionals import OptionalImports

optional_imports = OptionalImports()

from digitallab.helper.chunks import divide_into_chunks
from digitallab.helper.experiment_setting import ExperimentConfigs, ExperimentCollection
from digitallab.helper.experiment_validation import validate_if_experiments_eligible, validate_if_experiment_eligible
from digitallab.helper.generate_seeds import generate_seeds_from_experiment_collection
from digitallab.helper.output import *
from digitallab.helper.storage import DatabaseConnectInformation


def run_with_separate_interpreter(interpreter="python3", temporary_folder="./"):
    def remove_decorators_from_source_code(source_code):
        count = 0
        for line in source_code[0]:
            if line[0] == "@":
                count += 1
            else:
                break
        return source_code[0][count:]

    def build_python_file_text(source_code, ident, function_name):
        code = [
                   'import json\n',
                   'import traceback\n',
                   '\n',
               ] + remove_decorators_from_source_code(source_code) + [
                   '\n'
                   'with open("' + temporary_folder + 'dlab_tmp_config_' + ident + '.json") as f:\n',
                   '    config = json.load(f)\n',
                   'try:\n'
                   '    ret = ' + function_name + '(config)\n',
                   '    with open("' + temporary_folder + 'dlab_tmp_result_' + ident + '.json", "w") as json_file:\n',
                   '        json.dump(ret, json_file)\n',
                   'except Exception as e:\n',
                   '    error_string = traceback.format_exc()\n',
                   '    with open("' + temporary_folder + 'dlab_tmp_error_' + ident + '.txt", "w") as f:\n',
                   '        f.write(error_string)\n'
               ]
        return code

    def specialized_decorator(fn):
        @functools.wraps(fn)
        def wrapper(_config):
            salt = random.randint(-1e8, 1e8)
            ident = str(hash(frozenset(_config.items())) + hash(salt))
            while os.path.isfile(temporary_folder + "dlab_tmp_script_" + ident + ".py"):
                salt = random.randint(-1e8, 1e8)
                ident = str(hash(_config) + hash(salt))

            source_code = inspect.getsourcelines(fn)
            function_name = fn.__name__
            code = build_python_file_text(source_code, ident, function_name)
            with open(temporary_folder + "dlab_tmp_script_" + ident + ".py", "w") as f:
                for line in code:
                    f.write(line)
            with open(temporary_folder + "dlab_tmp_config_" + ident + ".json", "w") as json_file:
                json.dump(_config, json_file)
            status = os.system(interpreter + " " + temporary_folder + "dlab_tmp_script_" + ident + ".py")
            if status != 0:
                if os.path.isfile(temporary_folder + "dlab_tmp_config_" + ident + ".json"):
                    os.remove(temporary_folder + "dlab_tmp_config_" + ident + ".json")
                os.remove(temporary_folder + "dlab_tmp_script_" + ident + ".py")
                raise RuntimeError("Unknown error which could not be catched thrown by interpreter.")
            if os.path.isfile(temporary_folder + "dlab_tmp_error_" + ident + ".txt"):
                with open(temporary_folder + "dlab_tmp_error_" + ident + ".txt") as f:
                    error = f.readlines()
                os.remove(temporary_folder + "dlab_tmp_error_" + ident + ".txt")
                os.remove(temporary_folder + "dlab_tmp_config_" + ident + ".json")
                os.remove(temporary_folder + "dlab_tmp_script_" + ident + ".py")
                raise ChildProcessError("".join(error))
            with open(temporary_folder + "dlab_tmp_result_" + ident + ".json") as f:
                result = json.load(f)
            os.remove(temporary_folder + "dlab_tmp_result_" + ident + ".json")
            os.remove(temporary_folder + "dlab_tmp_config_" + ident + ".json")
            os.remove(temporary_folder + "dlab_tmp_script_" + ident + ".py")
            return result

        return wrapper

    return specialized_decorator


def check_eligible(chunk, database_connect_information):
    # TODO: require chunk[0] in parameters
    return validate_if_experiments_eligible(chunk[0], database_connect_information)


def prepare_and_run_experiment(config, ex, database_connect_information, config_to_str=str):
    error = None

    if validate_if_experiment_eligible(config, database_connect_information):
        with redirect_to_tqdm():
            if not ex.observers:
                if database_connect_information.has_mongodb_connection():
                    ex.observers.append(
                        MongoObserver(database_connect_information.mongodb_url,
                                      database_connect_information.mongodb_db))
                if database_connect_information.has_tinydb_connection():
                    ex.observers.append(
                        TinyDbObserver(database_connect_information.tinydb_path)
                    )
            ex.add_config(config)

            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                try:
                    ex.run(options={'--loglevel': 'CRITICAL'})
                except Exception as e:
                    error = e
            return True, config_to_str(config), error
    return False, config_to_str(config), error


class Lab:
    def __init__(self, name, config_to_string_func=str):
        self.__number_of_failed_instances = 0
        self.cache_id = None
        self.__retrieve_keys = None
        self.logger = None
        self.__database_storage = DatabaseConnectInformation()
        self.experiment_settings = None

        self.experiment_name = name
        self.__config_to_string_func = config_to_string_func
        self.__data_retrieval = None
        self.__force_use_of_cache = False

        self.__terminate_on_experiment_error = False

    def experiment(self, fn):
        experiment = Experiment(self.experiment_name, save_git_info=False)
        experiment.main(fn)
        database_connect_information = self.__database_storage
        config_to_string_func = str

        @functools.wraps(fn)
        def wrapper(config):
            return prepare_and_run_experiment(config, experiment, database_connect_information,
                                              config_to_str=config_to_string_func)

        return wrapper

    def run_experiments(self, experiment_function, experiment_settings: Union[str, dict, Iterable],
                        number_of_parallel_runs: int = 1, number_of_query_workers: int = 100,
                        number_of_query_chunks: int = 1000, path_to_log=None, show_selection_dialog=False,
                        terminate_on_experiment_error=False):
        self.__terminate_on_experiment_error = terminate_on_experiment_error
        self.__number_of_failed_instances = 0

        if path_to_log:
            self.__setup_logger(path_to_log)
        else:
            self.logger = None

        experiment_collection = ExperimentCollection(experiment_function, experiment_settings,
                                                     number_of_parallel_runs=number_of_parallel_runs,
                                                     number_of_query_chunks=number_of_query_chunks,
                                                     number_of_query_workers=number_of_query_workers,
                                                     show_selection_dialog=show_selection_dialog)

        seeds = generate_seeds_from_experiment_collection(experiment_collection)

        self.__get_configs_and_execute_experiments(experiment_collection, seeds)

    def add_mongodb_storage(self, url: str, database: str):
        if not optional_imports.mongodb_can_be_used():
            optional_imports.raise_pymongo_missing_error()
        self.__database_storage.setup_mongodb_connection(url, database)
        return self

    def add_tinydb_storage(self, tinydb_path: str):
        if not optional_imports.tinydb_can_be_used():
            optional_imports.raise_depencies_for_tinydb_missing_error()
        self.__database_storage.setup_tinydb_connection(tinydb_path)
        return self

    def set_keys_for_evaluation(self, keys_or_json_path: Union[dict, str]):
        self.__retrieve_keys = keys_or_json_path

    def __assert_storage(self):
        if not self.__database_storage.has_connection():
            raise IOError("No storage configured. Please add a mongoDB or tinyDB.")

    def __get_configs_and_execute_experiments(self, experiment_collection: ExperimentCollection, seeds):
        for experiment_setting in experiment_collection:
            self.__print_header(experiment_setting)
            configs = self.__generate_configs(experiment_setting, experiment_collection.number_of_query_chunks,
                                              experiment_collection.number_of_query_workers, seeds)
            if experiment_collection.number_of_parallel_runs > 1:
                self.__execute_experiments_in_parallel(configs, experiment_collection.experiment_function,
                                                       experiment_collection.number_of_parallel_runs)
            else:
                self.__execute_experiments_sequentially(configs, experiment_collection.experiment_function)
            self.__print_tail()

    def __print_tail(self):
        print("")
        print(self.__number_of_failed_instances, "experiments failed.")
        print("=" * 20)
        print("")

    @staticmethod
    def __print_header(experiment_setting):
        print("=" * 20)
        print("Starting sub-experiment:", experiment_setting.get_sub_experiment_name())
        print("")

    def __generate_configs(self, experiment_setting, number_of_query_chunks, number_of_query_workers, seeds):
        configs = self.__collect_possible_configs(seeds, experiment_setting)
        configs = self.__filter_eligible_configs(configs, number_of_query_chunks, number_of_query_workers)
        random.shuffle(configs)
        return configs

    def __execute_experiments_sequentially(self, configs, experiment_func):
        for experiment_was_run, config_to_string, error in tqdm(map(experiment_func, configs),
                                                                desc="Running experiments",
                                                                total=len(configs),
                                                                dynamic_ncols=True, file=sys.stdout, ascii=True,
                                                                colour="RED"):
            self.__log_experiment_infos(config_to_string, error, experiment_was_run)

    def __execute_experiments_in_parallel(self, configs, experiment_func, number_of_parallel_runs):
        with Pool(number_of_parallel_runs) as pool:
            for experiment_was_conducted, config_string, error in tqdm(pool.imap(experiment_func, configs, 5),
                                                                       desc="Running experiments", total=len(configs),
                                                                       dynamic_ncols=True):
                self.__log_experiment_infos(config_string, error, experiment_was_conducted)

    def __log_experiment_infos(self, config_string, error, experiment_was_conducted):
        if error is not None:
            if self.__terminate_on_experiment_error:
                raise error
            else:
                self.write_error_to_log(config_string, error)
                self.__number_of_failed_instances += 1
        self.write_log(experiment_was_conducted, config_string)

    def write_log(self, was_experiment_run, message):
        if self.logger:
            if was_experiment_run:
                self.logger.info("Finished Experiment:\n" + message)
            else:
                self.logger.info("Already running or finished:\n" + message)

    def write_error_to_log(self, config_string, error):
        if self.logger:
            self.logger.error("Error was thrown in config:\n" + config_string + "\n" + "\n".join(
                traceback.format_exception(type(error), error, error.__traceback__)))

    def __filter_eligible_configs(self, configs, number_of_query_chunks, number_of_query_workers):
        eligible = []
        chunks = divide_into_chunks(configs, number_of_query_chunks)
        with Pool(number_of_query_workers) as pool:
            for logic_chunk in tqdm(pool.imap(partial(
                    check_eligible, database_connect_information=self.__database_storage), chunks),
                    desc="Querying eligible experiments to run",
                    total=len(chunks), dynamic_ncols=True):
                eligible += logic_chunk
        configs = list(compress(configs, eligible))
        return configs

    @staticmethod
    def __collect_possible_configs(seeds, setting):
        configs = []
        configs_iterator = ExperimentConfigs(setting, seeds)
        total_estimated_seconds = 0
        timelimit_found = False
        with tqdm(total=len(setting), desc="Collecting possible experiments", dynamic_ncols=True) as pbar:
            for config in configs_iterator:
                if "timelimit" in config:
                    total_estimated_seconds += config["timelimit"]
                    timelimit_found = True
                if "time_limit" in config:
                    total_estimated_seconds += config["time_limit"]
                    timelimit_found = True
                configs.append(config)
                pbar.update(1)
        if timelimit_found:
            total_estimated_timedelta = datetime.timedelta(seconds=total_estimated_seconds)
            print("Found 'timelimit' or 'time_limit' in configs. Assuming you mean seconds and assuming each run takes "
                  "as long as the time limit allows, this computation would take ", str(total_estimated_timedelta), ".")
        return configs

    def __setup_logger(self, path_to_log):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False
        handler = RotatingFileHandler(path_to_log, maxBytes=1000)
        # set a formatter to include the level name
        handler.setFormatter(logging.Formatter(
            '[%(levelname)s] %(message)s'
        ))
        # add the journald handler to the current logger
        self.logger.addHandler(handler)

    def set_cache_id(self, name):
        self.cache_id = name

    def force_use_of_cache(self, b):
        self.__force_use_of_cache = b

    def __get_data_retrival(self, experiment_version):
        return DataRetrieval(self.experiment_name, experiment_version, self.__database_storage,
                             self.__retrieve_keys, self.cache_id, self.__force_use_of_cache)

    def get_recent_number_of_failed_instances(self):
        return self.__number_of_failed_instances

    def ecdf_plot(self, experiment_version):
        data_retrieval = self.__get_data_retrival(experiment_version)
        return ecdf_plot_class(AllExperimentsDatabaseCollector)(data_retrieval)

    def procedural_ecdf_plot(self, experiment_version):
        data_retrieval = self.__get_data_retrival(experiment_version)
        return ecdf_plot_class(ProceduralDatabaseCollector)(data_retrieval)

    def box_plot(self, experiment_version):
        data_retrieval = self.__get_data_retrival(experiment_version)
        return box_plot_class(AllExperimentsDatabaseCollector)(data_retrieval)

    def procedural_box_plot(self, experiment_version):
        data_retrieval = self.__get_data_retrival(experiment_version)
        return box_plot_class(ProceduralDatabaseCollector)(data_retrieval)

    def face_to_face_density_bar_plot(self, experiment_version):
        data_retrieval = self.__get_data_retrival(experiment_version)
        return FaceToFaceDensityBarPlot(data_retrieval)

    def mean_table(self, experiment_version):
        data_retrieval = self.__get_data_retrival(experiment_version)
        return MeanTable(data_retrieval)

    def median_table(self, experiment_version):
        data_retrieval = self.__get_data_retrival(experiment_version)
        return MedianTable(data_retrieval)

    def min_table(self, experiment_version):
        data_retrieval = self.__get_data_retrival(experiment_version)
        return MinTable(data_retrieval)

    def max_table(self, experiment_version):
        data_retrieval = self.__get_data_retrival(experiment_version)
        return MaxTable(data_retrieval)
