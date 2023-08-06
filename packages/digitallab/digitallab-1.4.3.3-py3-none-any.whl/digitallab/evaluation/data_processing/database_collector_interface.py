#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import abc
from collections import Iterable
from typing import Union

import numpy as np

from digitallab.evaluation.data_retrieval.retrieval import DataRetrieval
from digitallab.evaluation.helper.filter import filter_data

class DatabaseCollectorInterface(abc.ABC):
    def __init__(self, data_retrieval: DataRetrieval):
        self.data = None
        self._data_filter = {}
        self._data_retrieval = data_retrieval
        self._methods_key = None
        self._methods_key_print_label = None
        self._comparison_unit_filters = []

    def set_methods_key(self, key: str, label: Union[None, str] = None):
        assert isinstance(key, str)
        self._methods_key = key
        if label is None:
            self._methods_key_print_label = self._methods_key
        else:
            self._methods_key_print_label = label
        return self

    def _preprocess(self):
        self.data = self._data_retrieval.get_dataframe()
        comp_selection_or = np.zeros(len(self.data), dtype=bool)
        for d in self._comparison_unit_filters:
            comp_selection_and = np.ones(len(self.data), dtype=bool)
            for k, v in d.items():
                if not isinstance(v, str) and isinstance(v, Iterable):
                    comp_selection_and = comp_selection_and & (self.data[k].isin(v))
                else:
                    comp_selection_and = comp_selection_and & (self.data[k] == v)
            comp_selection_or = comp_selection_or | comp_selection_and
        self.data = self.data[comp_selection_or]

        if self._data_filter is not None:
            self.data = filter_data(self.data, **self._data_filter)

    def filter_data(self, **kwargs):
        self._data_filter = kwargs
        return self

    def _assert(self):
        assert self._methods_key and self._methods_key_print_label, "Set the label of the units to compare " \
                                                                    "before calling 'collect'. For " \
                                                                    "example if you want to compare different " \
                                                                    "methods and you have stored what method " \
                                                                    "was used in the field 'algorithm', you " \
                                                                    "set the label to 'algorithm'."

    @abc.abstractmethod
    def collect(self):
        self._assert()
        self._preprocess()
        return self.data
