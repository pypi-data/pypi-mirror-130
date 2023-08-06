#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import pandas as pd
from digitallab.evaluation.data_processing.database_collector_interface import DatabaseCollectorInterface

from digitallab.evaluation.data_processing.all_experiments_database_collector import \
    AllExperimentsDatabaseCollectorSkeleton
from digitallab.evaluation.data_processing.facetoface_database_collector import FaceToFaceDatabaseCollectorSkeleton
from digitallab.evaluation.data_retrieval.retrieval import DataRetrieval


class ProceduralDatabaseCollector(FaceToFaceDatabaseCollectorSkeleton, AllExperimentsDatabaseCollectorSkeleton):
    def __init__(self, data_retrieval: DataRetrieval):
        super().__init__(data_retrieval)
        self._procedure = None
        self._procedure_outcome_label = None

    def add_unit_to_compare(self, label, **kwargs):
        self._add_face(**kwargs)
        self._add_unit_to_compare(label, **kwargs)
        return self

    def set_procedure_on_methods(self, function, outcome_label):
        self._procedure = function
        self._procedure_outcome_label = outcome_label
        return self

    def set_attribute_to_give_to_procedure(self, key):
        self.set_pivot(key)
        return self

    def __assert(self):
        FaceToFaceDatabaseCollectorSkeleton._assert(self)
        AllExperimentsDatabaseCollectorSkeleton._assert(self)
        assert self._procedure, "'set_procedure_on_methods' must be called' before 'collect' is called."

    def collect(self) -> pd.DataFrame:
        self.__assert()
        DatabaseCollectorInterface.collect(self)

        self._comparison_unit_filters = self._faces
        self._preprocess()

        self.data = self.data.pivot_table(index=self._pivot_index_columns, columns=self._methods_key,
                                          values=self._pivot_value_key)

        if self._drop_na:
            self.data = self.data.dropna()

        methods = set([comparison_unit[self._methods_key] for comparison_unit in self._comparison_unit_filters])

        for column_being_processed in methods:
            def apply_function_to_row(row):
                kwargs = {method: row.at[method] for method in methods}
                return self._procedure(row.at[column_being_processed], **kwargs)

            self.data[column_being_processed + "_new"] = self.data.apply(apply_function_to_row, axis=1)

        self.data = self.data.drop(methods, axis=1)

        self.data.rename({method + "_new": method for method in methods}, inplace=True, axis=1)

        self.data.reset_index(inplace=True)

        self.data = pd.melt(self.data, id_vars=self._pivot_index_columns, value_vars=methods,
                            var_name=self._methods_key, value_name=self._procedure_outcome_label)

        self._replace_comparison_unit_names_with_labels()

        return self.data
