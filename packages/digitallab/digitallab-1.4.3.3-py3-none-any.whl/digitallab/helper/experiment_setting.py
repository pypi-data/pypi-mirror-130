#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
import os
from collections import Iterable
from typing import Union

from pick import pick


class ExperimentConfigs:
    def __init__(self, experiment_setting, seeds):
        self.experiment_setting = experiment_setting
        self.seeds = seeds

    def __len__(self):
        return len(self.experiment_setting)

    def __iter__(self):
        for conf in self.experiment_setting:
            for i in range(conf["number_of_repetitions"]):
                modified_conf = dict(conf)
                modified_conf["id"] = i
                modified_conf["seed"] = self.seeds[i]
                yield modified_conf


class ExperimentSettingIterator:
    def __init__(self, experiment_setting):
        self.experiment_setting = experiment_setting

        self.__iterators = dict()
        self.__setup_iterator_list()
        self.__current_config = dict()
        self.__setup_first_config()
        self.__first_iteration = True
        self.__stop = False

    def __setup_iterator_list(self):
        for key in self.experiment_setting.keys:
            self.__setup_iterator(key)

    def __setup_iterator(self, key):
        if isinstance(self.experiment_setting.setting[key], list):
            self.__iterators[key] = iter(self.experiment_setting.setting[key])

    def __deep_copy_current_config(self):
        config = dict()
        for key in self.experiment_setting.keys:
            config[key] = self.__current_config[key]
        return config

    def __next__(self):
        if self.__stop:
            raise StopIteration
        config = self.__deep_copy_current_config()
        try:
            self.__generate_next_config()
        except StopIteration:
            self.__stop = True
        return config

    def __setup_first_config(self):
        for key in self.experiment_setting.keys:
            if key in self.__iterators.keys():
                self.__next_config_key(key)
            else:
                self.__current_config[key] = self.experiment_setting.setting[key]

    def __generate_next_config(self):
        for key in self.experiment_setting.keys:
            if key in self.__iterators.keys():
                try:
                    self.__next_config_key(key)
                    return
                except StopIteration:
                    self.__setup_iterator(key)
                    self.__next_config_key(key)
        raise StopIteration

    def __next_config_key(self, key):
        self.__current_config[key] = next(self.__iterators[key])


class ExperimentCollection:
    def __init__(self, experiment_function, path_to_jsons_or_collection_of_dicts: Union[str, dict, Iterable],
                 number_of_parallel_runs=1, number_of_query_workers=100, number_of_query_chunks=100,
                 show_selection_dialog=False):
        self.experiment_function = experiment_function
        self.number_of_parallel_runs = number_of_parallel_runs
        self.number_of_query_workers = number_of_query_workers
        self.number_of_query_chunks = number_of_query_chunks

        self.experiment_settings = []
        self.__build_experiment_settings(path_to_jsons_or_collection_of_dicts,
                                         show_selection_dialog=show_selection_dialog)

    def __build_experiment_settings(self, path_to_jsons_or_collection_of_dicts, show_selection_dialog=False):
        if isinstance(path_to_jsons_or_collection_of_dicts, str):
            self.__build_experiment_settings_from_path(path_to_jsons_or_collection_of_dicts,
                                                       show_selection_dialog=show_selection_dialog)
        elif isinstance(path_to_jsons_or_collection_of_dicts, dict):
            self.experiment_settings.append(ExperimentSetting(path_to_jsons_or_collection_of_dicts))
        elif isinstance(path_to_jsons_or_collection_of_dicts, Iterable):
            self.__build_experiment_settings_from_iterable(path_to_jsons_or_collection_of_dicts,
                                                           show_selection_dialog=show_selection_dialog)
        else:
            raise ValueError(
                "'path_to_jsons_or_collection_of_dicts' must be a string, a dictionary or an iterable object.")

    def __build_experiment_settings_from_path(self, path_to_jsons, show_selection_dialog=False):
        if os.path.isdir(path_to_jsons):
            self.experiment_settings = self.__get_eligible_settings_in_directory(path_to_jsons,
                                                                                 show_selection_dialog=show_selection_dialog)
        if os.path.isfile(path_to_jsons):
            self.experiment_settings.append(ExperimentSetting(path_to_jsons))

    def __build_experiment_settings_from_iterable(self, collection_of_dicts, show_selection_dialog=False):
        collected_settings = []
        for element in collection_of_dicts:
            assert isinstance(element, dict), "The collection does not contain dictionaries only."
            collected_settings.append(ExperimentSetting(element))
        if show_selection_dialog:
            self.experiment_settings = self.__show_dialog_and_filter_settings(collected_settings)
        else:
            self.experiment_settings = collected_settings

    @staticmethod
    def __get_eligible_settings_in_directory(directory, show_selection_dialog=False):
        collected_settings = ExperimentCollection.__collect_all_settings_in_directory(directory)
        if show_selection_dialog:
            return ExperimentCollection.__show_dialog_and_filter_settings(collected_settings)
        else:
            return collected_settings

    @staticmethod
    def __show_dialog_and_filter_settings(collected_settings):
        title = "Please choose the experiments to run (press SPACE to mark, ENTER to continue): "

        def option_to_string(setting):
            return setting.get_experiment_name() + ": " + setting.get_sub_experiment_name() + "(" + \
                   setting.get_version() + ")"

        selected = pick(collected_settings, title, multiselect=True, min_selection_count=1,
                        options_map_func=option_to_string)
        return [element[0] for element in selected]

    @staticmethod
    def __collect_all_settings_in_directory(directory):
        collected_settings = []
        if os.path.isdir(directory):
            for path, dirs, files in os.walk(directory):
                for file in files:
                    ext = os.path.splitext(file)[-1].lower()
                    if ext == ".json":
                        setting = ExperimentSetting(path + "/" + file)
                        collected_settings.append(setting)
        return collected_settings

    def __iter__(self):
        return self.experiment_settings.__iter__()

    def __len__(self):
        return len(self.experiment_settings)


class ExperimentSetting:
    def __init__(self, json_file_path_or_dict: Union[str, dict]):
        if isinstance(json_file_path_or_dict, str):
            with open(json_file_path_or_dict) as json_file:
                self.setting = json.load(json_file)
        elif isinstance(json_file_path_or_dict, dict):
            self.setting = json_file_path_or_dict
        else:
            raise TypeError("Argument must be either a string or a dictonary.")
        self.keys = list(self.setting.keys())

    def __len__(self):
        count = 1
        for key in self.keys:
            try:
                if isinstance(self.setting[key], list):
                    count *= len(self.setting[key])
            except TypeError:
                count *= 1
        count *= self.setting["number_of_repetitions"]
        return count

    def number_of_unique_experiments(self):
        count = 1
        for key in self.keys:
            try:
                if isinstance(self.setting[key], list):
                    count *= len(self.setting[key])
            except TypeError:
                count *= 1
        return count

    def __iter__(self):
        return ExperimentSettingIterator(self)

    def get_experiment_name(self):
        return self.setting["experiment"]

    def get_sub_experiment_name(self):
        return self.setting["sub_experiment"]

    def get_version(self):
        return self.setting["version"]
