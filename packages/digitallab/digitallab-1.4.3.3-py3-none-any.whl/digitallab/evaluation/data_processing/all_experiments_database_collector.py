#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import abc

from digitallab.evaluation.data_processing.database_collector_interface import DatabaseCollectorInterface
from digitallab.evaluation.data_processing.procedural_columns import ProceduralColumns
from digitallab.evaluation.data_retrieval.retrieval import DataRetrieval


class AllExperimentsDatabaseCollectorSkeleton(DatabaseCollectorInterface, abc.ABC):
    def __init__(self, data_retrieval: DataRetrieval):
        super().__init__(data_retrieval)
        self._names_of_comparison_units = list()

    def _add_unit_to_compare(self, label, **kwargs):
        self._comparison_unit_filters.append(kwargs)
        self._names_of_comparison_units.append(label)
        return self

    def get_label_of_comparison_unit(self, method):
        for looked_up_method, label in zip(
                [comparison_unit["method"] for comparison_unit in self._comparison_unit_filters],
                self._names_of_comparison_units):
            if looked_up_method == method:
                return label

    def _assert(self):
        assert self._names_of_comparison_units and self._comparison_unit_filters, \
            "You have call 'add_unit_to_compare' at least one time " \
            "before calling 'process'."

    @abc.abstractmethod
    def collect(self):
        return super().collect()

    def _replace_comparison_unit_names_with_labels(self):
        replace_dict = dict()
        for comparison_filter, name in zip(self._comparison_unit_filters, self._names_of_comparison_units):
            if name:
                replace_dict[comparison_filter["method"]] = name
        self.data[self._methods_key] = self.data[self._methods_key].replace(replace_dict)


class AllExperimentsDatabaseCollector(AllExperimentsDatabaseCollectorSkeleton, ProceduralColumns):
    def __init__(self, data_retrieval: DataRetrieval):
        AllExperimentsDatabaseCollectorSkeleton.__init__(self, data_retrieval)
        ProceduralColumns.__init__(self)

    def add_unit_to_compare(self, label, **kwargs):
        self._add_unit_to_compare(label, **kwargs)
        return self

    def collect(self):
        self._assert()
        AllExperimentsDatabaseCollectorSkeleton.collect(self)
        self.data = self._process_procedural_columns(self.data)
        self._replace_comparison_unit_names_with_labels()

        return self.data
