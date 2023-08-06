#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import os
from unittest import TestCase

from digitallab.lab import Lab
from digitallab.tests.experiments_for_tests import *

lab = Lab("test").add_tinydb_storage("test_tiny")


@lab.experiment
def main(_config):
    if _config["method"] == "fast":
        return fast(_config)
    elif _config["method"] == "slow":
        return slow(_config)
    elif _config["method"] == "special":
        return special(_config)


def relative_time(low, high):
    return low / high


class TestFaceToFaceDensityBarPlotPlot(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not os.path.isdir("test_tiny"):
            lab.run_experiments(main, [standard_setting, special_setting], number_of_query_chunks=100,
                                number_of_parallel_runs=1, number_of_query_workers=1)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("face_to_face_bar_plot_test.pdf")

    def test_plot_shows_without_errors(self):
        lab.face_to_face_density_bar_plot("1"). \
            set_methods_key("method"). \
            set_index_columns(["id", "instance"]). \
            set_pivot("runtime"). \
            set_first_face("Fast", method="fast"). \
            set_second_face("Slow", method="slow"). \
            add_procedural_column("runtime_quotient", relative_time, "slow", "fast"). \
            set_value_of_interest("runtime_quotient", "Low run time / High run time"). \
            save("face_to_face_bar_plot_test.pdf")
