#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import abc
from typing import Union
import matplotlib.pyplot as plt


class PlotSkeleton(abc.ABC):
    def __init__(self):
        self._use_grid = False
        self.dpi = None
        self._legend_is_hidden = False
        self.font_scale = 1
        self._xaxis_label = None
        self._yaxis_label = None
        self._x_range = None
        self._y_range = None

        self._x_label_hidden = False
        self._y_label_hidden = False

        self._x_scale = None
        self._y_scale = None

        self._hue_order = None

        self._sharey = True
        self._sharex = True

        self._grid_row_key = None
        self._grid_col_key = None
        self._grid_row_label = None
        self._grid_col_label = None

        self.save_file_name = None
        self.save_fig_size = None

    def set_save_fig_size(self, size: Union[str, tuple]):
        if isinstance(size, str):
            if size == "a3":
                self.save_fig_size = (10, 6.18)
            else:
                raise KeyError("save_fig_size '" + str(self.save_fig_size) + "' not known.")
        else:
            self.save_fig_size = size
        return self

    def set_yaxis_label(self, label):
        self._yaxis_label = label
        return self

    def set_xaxis_label(self, label):
        self._xaxis_label = label
        return self

    def set_share_x_axis(self, b: bool):
        self._sharex = b
        return self

    def set_share_y_axis(self, b: bool):
        self._sharey = b
        return self

    def hide_legend(self, b):
        self._legend_is_hidden = b
        return self

    def set_dpi(self, d):
        self.dpi = d
        return self

    def set_font_scale(self, s):
        self.font_scale = s
        return self

    def add_grid(self, *args, col_label=None, row_label=None, sharex=True, sharey=True):
        self._use_grid = True
        self._grid_col_key = args[0]
        if len(args) > 1:
            self._grid_row_key = args[1]
        self._grid_col_label = col_label
        self._grid_row_label = row_label
        self._sharex = sharex
        self._sharey = sharey

        return self

    def set_x_scale(self, scale):
        self._x_scale = scale
        return self

    def set_y_scale(self, scale):
        self._y_scale = scale
        return self

    def set_x_log_scale(self, b):
        self._x_scale = "log" if b else None
        return self

    def set_y_log_scale(self, b):
        self._y_scale = "log" if b else None
        return self

    def set_x_range(self, range):
        self._x_range = range
        return self

    def set_y_range(self, range):
        self._y_range = range
        return self

    def hide_xlabel(self, b):
        self._x_label_hidden = b
        return self

    def hide_ylabel(self, b):
        self._y_label_hidden = b
        return self

    def set_hue_order(self, order):
        self._hue_order = order
        return self

    def _decorate_axis(self, ax):
        if self._y_range is not None:
            ax.set_ylim(self._y_range)

        if self._x_range is not None:
            ax.set_xlim(self._x_range)

        if self._x_label_hidden or not self._xaxis_label:
            ax.set_xlabel("")
        else:
            ax.set_xlabel(self._xaxis_label)

        if self._y_label_hidden or not self._yaxis_label:
            ax.set_ylabel("")
        else:
            ax.set_ylabel(self._yaxis_label)

        if self._x_scale:
            ax.set(xscale=self._x_scale)

        if self._y_scale:
            ax.set(yscale=self._y_scale)

    def _decorate_axes(self, axes):
        for axis in axes.flat:
            self._decorate_axis(axis)

    @abc.abstractmethod
    def build_axes_without_grid(self):
        pass

    @abc.abstractmethod
    def build_axes_with_grid(self):
        pass

    @abc.abstractmethod
    def build_legend_for_non_grid(self, axes):
        pass

    @abc.abstractmethod
    def build_legend_for_grid(self, axes):
        pass

    def save(self, file_path: str, size="a3"):
        plt.clf()
        self.set_save_fig_size(size)
        plt.figure(figsize=self.save_fig_size)
        self._build_axes()
        fig = plt.gcf()
        fig.set_size_inches(self.save_fig_size)
        plt.savefig(file_path, dpi=self.dpi)

    def _build_axes(self):
        if self._use_grid:
            self.build_axes_with_grid()
        else:
            self.build_axes_without_grid()

    def plot(self):
        plt.clf()
        self._build_axes()
        if not self._use_grid:
            plt.tight_layout()
        plt.show()
