#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import colorsys

import matplotlib.colors as mc
import seaborn as sns

from digitallab.evaluation.data_retrieval.retrieval import DataRetrieval
from digitallab.evaluation.plots.aggregate_plot_skeleton import xy_aggregate_plot_skeleton


def box_plot_class(DatabaseCollector):
    class BoxPlot(xy_aggregate_plot_skeleton(DatabaseCollector)):
        def __init__(self, data_retrieval: DataRetrieval):
            super().__init__(data_retrieval)

        def build_axes_without_grid(self):
            sns.set(style="whitegrid", palette="colorblind", font_scale=self.font_scale)
            super().collect()

            ax = sns.boxplot(x=self._xaxis, y=self._yaxis, hue=self._methods_key_print_label,
                             data=self.data, hue_order=self._names_of_comparison_units, orient="v")

            self._decorate_axis(ax)
            self.decorate_box_plots(ax)
            if self._legend_is_hidden:
                ax.legend('', frameon=False)
            else:
                ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

        def build_axes_with_grid(self):
            sns.set(style="whitegrid", palette="colorblind", font_scale=self.font_scale)
            super().collect()

            if self._grid_row_key is not None:
                facet_grid = sns.catplot(x=self._xaxis, y=self._yaxis, hue=self._methods_key_print_label,
                                         data=self.data,
                                         col=self._grid_col_key if self._grid_col_label is None else self._grid_col_label,
                                         row=self._grid_row_key if self._grid_row_label is None else self._grid_row_label,
                                         kind="box", sharex=self._sharex, sharey=self._sharey,
                                         legend=(not self._legend_is_hidden),
                                         hue_order=self.get_order_of_methods())
            else:
                facet_grid = sns.catplot(x=self._xaxis, y=self._yaxis, hue=self._methods_key_print_label,
                                         data=self.data,
                                         col=self._grid_col_key if self._grid_col_label is None else self._grid_col_label,
                                         kind="box", sharex=self._sharex, sharey=self._sharey,
                                         legend=(not self._legend_is_hidden),
                                         hue_order=self.get_order_of_methods())

            for ax in facet_grid.axes.flat:
                self.decorate_box_plots(ax)
            self._decorate_axes(facet_grid.axes)
            facet_grid.set(xlabel="" if self._x_label_hidden else self._xaxis_label,
                           ylabel="" if self._y_label_hidden else self._yaxis_label)

        @staticmethod
        def decorate_box_plots(ax):
            for i, artist in enumerate(ax.artists):
                col = BoxPlot.darken_color(artist.get_facecolor(), 0.3)
                artist.set_edgecolor(artist.get_facecolor())

                # Each box has 6 associated Line2D objects (to make the whiskers, fliers, etc.)
                # Loop over them here, and use the same colour as above
                for j in range(i * 6, i * 6 + 6):
                    line = ax.lines[j]
                    line.set_color(col)
                    line.set_mfc(col)
                    line.set_mec(col)
                    if j == i * 6 + 4:
                        line.set_linewidth(3)  # ADDITIONAL ADJUSTMENT

        @staticmethod
        def darken_color(color, amount=0.5):
            try:
                c = mc.cnames[color]
            except:
                c = color
            c = colorsys.rgb_to_hls(*mc.to_rgb(c))
            return colorsys.hls_to_rgb(c[0], c[1] - amount * (c[1]), c[2])

    return BoxPlot
