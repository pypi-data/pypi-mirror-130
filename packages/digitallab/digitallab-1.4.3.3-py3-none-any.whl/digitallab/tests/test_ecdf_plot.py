#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from unittest import TestCase

from matplotlib.testing import set_reproducibility_for_testing

from digitallab.lab import Lab
from digitallab.tests.cleanup import *
from digitallab.tests.experiments_for_tests import *

set_reproducibility_for_testing()

from matplotlib.testing.compare import compare_images

lab = Lab("test").add_tinydb_storage("test_tiny")


@lab.experiment
def main(_config):
    if _config["method"] == "fast":
        return fast(_config)
    elif _config["method"] == "slow":
        return slow(_config)
    elif _config["method"] == "special":
        return special(_config)


class TestECDFPlot(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not os.path.isdir("test_tiny"):
            lab.run_experiments(main, [standard_setting, special_setting], number_of_query_chunks=100,
                                number_of_parallel_runs=1, number_of_query_workers=1)
        cls.test_number = 0

    @classmethod
    def tearDownClass(cls) -> None:
        clean_up_temporary_test_pdfs()
        clean_up_reference_pdf_directory("ecdf_reference_pdfs")

    def test_ecdf_plot_produces_correct_pdf(self):
        simple_ecdf_plot("test.pdf")
        self.assertIsNone(compare_images("ecdf_reference_pdfs/ecdf_plot_produces_correct_pdf.pdf", "test.pdf", 0))

    def test_plot_order_does_not_matter(self):
        switched_order_ecdf_plot("test.pdf")
        self.assertIsNone(compare_images("ecdf_reference_pdfs/plot_order_does_not_matter.pdf", "test.pdf", 0))

    def test_grid_produces_correct_plot(self):
        grid_ecdf_plot("test.pdf")
        self.assertIsNone(compare_images("ecdf_reference_pdfs/grid_produces_correct_plot.pdf", "test.pdf", 0))

    def test_hue_order(self):
        with self.subTest("Fast, Slow hue order"):
            hue_order_ecdf_plot("test_1.pdf", ["fast", "slow"])
            self.assertIsNone(compare_images("ecdf_reference_pdfs/fast_slow_hue_order.pdf", "test_1.pdf", 0))

        with self.subTest("Slow, Fast hue order"):
            hue_order_ecdf_plot("test_2.pdf", ["slow", "fast"])
            self.assertIsNone(compare_images("ecdf_reference_pdfs/slow_fast_hue_order.pdf", "test_2.pdf", 0))

    def test_no_legend_shows_correctly(self):
        no_legend_ecdf_plot("test.pdf")
        compare_images("ecdf_reference_pdfs/no_legend.pdf", "test.pdf", 0)


def simple_ecdf_plot(file_path):
    lab.ecdf_plot("1"). \
        set_methods_key("method", "Method"). \
        set_value_of_interest("runtime", "Run time in seconds"). \
        add_unit_to_compare("Slow", method="slow"). \
        add_unit_to_compare("Fast", method="fast"). \
        set_yaxis_label("Proportion of solved instances"). \
        set_font_scale(1). \
        set_save_fig_size("a3"). \
        save(file_path)


def switched_order_ecdf_plot(file_path):
    lab.ecdf_plot("1"). \
        set_methods_key("method", "Method"). \
        set_value_of_interest("runtime", "Run time in seconds"). \
        add_unit_to_compare("Fast", method="fast"). \
        add_unit_to_compare("Slow", method="slow"). \
        set_yaxis_label("Proportion of solved instances"). \
        set_font_scale(1). \
        set_save_fig_size("a3"). \
        save(file_path)


def grid_ecdf_plot(file_path):
    lab.ecdf_plot("1"). \
        set_methods_key("method", "Method"). \
        set_value_of_interest("runtime", "Run time in seconds"). \
        add_unit_to_compare("Slow", method="slow"). \
        add_unit_to_compare("Fast", method="fast"). \
        set_yaxis_label("Proportion of solved instances"). \
        add_grid("instance"). \
        set_font_scale(1). \
        set_save_fig_size("a3"). \
        save(file_path)


def hue_order_ecdf_plot(file_path, hue_order):
    lab.ecdf_plot("1"). \
        set_methods_key("method", "Method"). \
        set_value_of_interest("runtime", "Run time in seconds"). \
        add_unit_to_compare("Fast", method="fast"). \
        add_unit_to_compare("Slow", method="slow"). \
        set_yaxis_label("Proportion of solved instances"). \
        set_font_scale(1). \
        set_save_fig_size("a3"). \
        set_hue_order(hue_order). \
        save(file_path)


def no_legend_ecdf_plot(file_path):
    lab.ecdf_plot("1"). \
        set_methods_key("method", "Method"). \
        set_value_of_interest("runtime", "Run time in seconds"). \
        add_unit_to_compare("Fast", method="fast"). \
        add_unit_to_compare("Slow", method="slow"). \
        set_yaxis_label("Proportion of solved instances"). \
        set_font_scale(1). \
        set_save_fig_size("a3"). \
        hide_legend(True). \
        save(file_path)
