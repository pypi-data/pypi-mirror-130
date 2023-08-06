#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


class ProceduralColumns:
    def __init__(self):
        self._procedural_col_names = []
        self._procedural_col_funcs = []
        self._procedural_col_input_cols = []

    def add_procedural_column(self, col_name, func, *args):
        self._procedural_col_names.append(col_name)
        self._procedural_col_funcs.append(func)
        self._procedural_col_input_cols.append(args)
        return self

    def _process_procedural_columns(self, data):
        for col_name, func, input_cols in zip(self._procedural_col_names, self._procedural_col_funcs,
                                              self._procedural_col_input_cols):
            def apply_function_to_row(row):
                arguments = [row.at[col] for col in list(input_cols)]
                return func(*arguments)

            data[col_name] = data.apply(apply_function_to_row, axis=1)
        return data
