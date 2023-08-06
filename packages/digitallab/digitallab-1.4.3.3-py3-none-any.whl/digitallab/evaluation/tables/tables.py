#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from digitallab.evaluation.tables.table_skeleton import TableSkeleton
import numpy as np


class MeanTable(TableSkeleton):
    def build_table(self):
        self.collect()
        table = self.data.pivot_table(values=self._pivot_value_key, index=self._instance_keys_print_labels,
                                      columns=self._methods_key_print_label, aggfunc=np.mean)
        return table


class MedianTable(TableSkeleton):
    def build_table(self):
        self.collect()
        table = self.data.pivot_table(values=self._pivot_value_key, index=self._instance_keys_print_labels,
                                      columns=self._methods_key_print_label, aggfunc=np.median)
        return table


class MinTable(TableSkeleton):
    def build_table(self):
        self.collect()
        table = self.data.pivot_table(values=self._pivot_value_key, index=self._instance_keys_print_labels,
                                      columns=self._methods_key_print_label, aggfunc=np.min)
        return table


class MaxTable(TableSkeleton):
    def build_table(self):
        self.collect()
        table = self.data.pivot_table(values=self._pivot_value_key, index=self._instance_keys_print_labels,
                                      columns=self._methods_key_print_label, aggfunc=np.max)
        return table
