#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import abc
from typing import Iterable, Union

import numpy as np

from digitallab.evaluation.data_processing.all_experiments_database_collector import AllExperimentsDatabaseCollector
from digitallab.evaluation.data_retrieval.retrieval import DataRetrieval


class TableSkeleton(AllExperimentsDatabaseCollector, abc.ABC):
    def __init__(self, data_retrieval: DataRetrieval):
        super().__init__(data_retrieval)
        self._save_path = None
        self._highlight_min = False
        self._highlight_max = False

        self._instance_keys = None
        self._instance_keys_print_labels = None

        self._pivot_value_key = None

    def set_instance_keys(self, keys: Iterable, labels: Union[None, Iterable] = None):
        assert isinstance(keys, Iterable), "The parameter 'keys' is not iterable."
        assert isinstance(labels, Iterable) or labels is None, "The parameter 'labels' is not iterable."
        self._instance_keys = keys
        if labels is None:
            self._instance_keys_print_labels = keys
        else:
            self._instance_keys_print_labels = labels
        return self

    def set_value_of_interest(self, key: str):
        self._pivot_value_key = key
        return self

    def set_highlight_min(self, b):
        self._highlight_min = b
        if b:
            self._highlight_max = False

    def set_highlight_max(self, b):
        self._highlight_max = b
        if b:
            self._highlight_min = False

    def _assert(self):
        pass

    def collect(self):
        self._assert()
        super().collect()
        self.__rename_instances()
        self.__rename_method()

    def __rename_instances(self):
        rename_dict = {key: label for key, label in
                       zip(self._instance_keys, self._instance_keys_print_labels)}
        self.data.rename(columns=rename_dict, inplace=True)

    def __rename_method(self):
        rename_dict = dict()
        rename_dict[self._methods_key] = self._methods_key_print_label
        self.data.rename(columns=rename_dict, inplace=True)

    @abc.abstractmethod
    def build_table(self):
        pass

    def set_save_path(self, path):
        self._save_path = path