#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from digitallab.tests.test_ecdf_plot import *

from matplotlib.testing import set_reproducibility_for_testing
set_reproducibility_for_testing()

if __name__ == '__main__':
    dir = "ecdf_reference_pdfs/"

    simple_ecdf_plot(dir + "ecdf_plot_produces_correct_pdf.pdf")
    grid_ecdf_plot(dir + "grid_produces_correct_plot.pdf")
    switched_order_ecdf_plot(dir + "plot_order_does_not_matter.pdf")
    hue_order_ecdf_plot(dir + "fast_slow_hue_order.pdf", ["fast", "slow"])
    hue_order_ecdf_plot(dir + "slow_fast_hue_order.pdf", ["slow", "fast"])
    no_legend_ecdf_plot(dir + "no_legend.pdf")

    dir = "box_plots_reference_pdfs/"


