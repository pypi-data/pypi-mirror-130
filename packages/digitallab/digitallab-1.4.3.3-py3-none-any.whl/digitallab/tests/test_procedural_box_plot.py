#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import os
from unittest import TestCase
import importlib

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


def performance_ratio(runtime, **kwargs):
    return runtime / min(kwargs.values())


class TestECDFPlot(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not os.path.isdir("test_tiny"):
            lab.run_experiments(main, [standard_setting, special_setting], number_of_query_chunks=100,
                                number_of_parallel_runs=1, number_of_query_workers=1)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("box_plot_test.pdf")
        os.remove("box_plot_grid_test.pdf")

    def test_plot_shows_without_errors(self):
        lab.procedural_box_plot("1"). \
            set_procedure_on_methods(performance_ratio, "performance_ratio"). \
            set_attribute_to_give_to_procedure("runtime"). \
            set_index_columns(["id", "instance"]). \
            set_methods_key("method", "Method"). \
            add_unit_to_compare("Slow", method="slow"). \
            add_unit_to_compare("Fast", method="fast"). \
            set_yaxis("performance_ratio", "Performance ratio"). \
            set_xaxis("instance", "Instance"). \
            set_font_scale(1). \
            set_save_fig_size("a3"). \
            save("box_plot_test.pdf")

    def test_plot_order_does_not_matter(self):
        lab.procedural_box_plot("1"). \
            set_procedure_on_methods(performance_ratio, "performance_ratio"). \
            set_attribute_to_give_to_procedure("runtime"). \
            set_index_columns(["id", "instance"]). \
            set_methods_key("method", "Method"). \
            add_unit_to_compare("Fast", method="fast"). \
            add_unit_to_compare("Slow", method="slow"). \
            set_yaxis("performance_ratio", "Performance ratio"). \
            set_xaxis("instance", "Instance"). \
            set_font_scale(1). \
            set_save_fig_size("a3"). \
            save("box_plot_test.pdf")

    def test_grid_works_without_errors(self):
        lab.procedural_box_plot("1"). \
            set_procedure_on_methods(performance_ratio, "performance_ratio"). \
            set_attribute_to_give_to_procedure("runtime"). \
            set_index_columns(["id", "instance"]). \
            set_methods_key("method", "Method"). \
            add_unit_to_compare("Slow", method="slow"). \
            add_unit_to_compare("Fast", method="fast"). \
            set_yaxis("performance_ratio", "Performance ratio"). \
            set_xaxis("instance", "Instance"). \
            add_grid("instance"). \
            set_font_scale(1). \
            set_save_fig_size("a3"). \
            save("box_plot_grid_test.pdf")
