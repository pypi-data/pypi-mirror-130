#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from collections import Iterable

import pandas as pd
import abc

from digitallab.evaluation.data_processing.database_collector_interface import DatabaseCollectorInterface
from digitallab.evaluation.data_processing.procedural_columns import ProceduralColumns
from digitallab.evaluation.data_retrieval.retrieval import DataRetrieval


class FaceToFaceDatabaseCollectorSkeleton(DatabaseCollectorInterface, abc.ABC):
    def __init__(self, data_retrieval: DataRetrieval):
        super().__init__(data_retrieval)
        self._faces = []
        self._pivot_index_columns = None
        self._pivot_value_key = None
        self._drop_na = False

    def _add_face(self, **kwargs):
        self._faces.append(kwargs)
        return self

    def set_index_columns(self, index_cols: Iterable):
        """
        Set the name of the variables/columns which uniquely define similar runs/settings.

        Args:
            index_cols: A collection of strings determining the names of the identifying columns
        """
        self._pivot_index_columns = index_cols
        return self

    def set_pivot(self, key):
        self._pivot_value_key = key
        return self

    def drop_na(self, b):
        self.__drop_na = b
        return self

    def _assert(self):
        assert self._pivot_index_columns, "The method 'set_index_columns' was not called before 'process'."
        assert self._pivot_value_key, "The method 'pivot' was not called before 'process'."
        assert self._faces, "The method 'add_face' must be called at least one time before calling 'process'."
        for face in self._faces:
            assert self._methods_key in face.keys(), "Each face must include the method key as a dictionary key."
        method_values = {face[self._methods_key] for face in self._faces}
        assert len(method_values) == len(self._faces), "Multiple faces have the same value for the key '" + \
                                                       self._methods_key + "'."

    @abc.abstractmethod
    def collect(self):
        return super().collect()


class FaceToFaceDatabaseCollector(FaceToFaceDatabaseCollectorSkeleton, ProceduralColumns):
    def __init__(self, data_retrieval: DataRetrieval):
        FaceToFaceDatabaseCollectorSkeleton.__init__(self, data_retrieval)
        ProceduralColumns.__init__(self)

    def add_face(self, **kwargs):
        self._add_face(**kwargs)
        return self

    def collect(self) -> pd.DataFrame:
        self._assert()
        self._comparison_unit_filters = self._faces
        FaceToFaceDatabaseCollectorSkeleton.collect(self)

        self.data = self.data.pivot_table(index=self._pivot_index_columns, columns=self._methods_key,
                                          values=self._pivot_value_key)

        if self._drop_na:
            self.data = self.data.dropna()

        self.data = self._process_procedural_columns(self.data)

        return self.data
