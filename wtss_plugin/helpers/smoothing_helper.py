#
# This file is part of Python QGIS Plugin for WTSS.
# Copyright (C) 2024 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#

"""Python QGIS Plugin for WTSS."""

import matplotlib.pyplot as plt
import numpy as np
import seaborn
from pygam import LinearGAM, s
from scipy.signal import savgol_filter
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

from ..helpers.pystac_helper import get_source_from_click


class SGolay:
    """Savitz Golay Smothing."""

    def __init__(self, window_size: int, polynomial_order: int, mode: str = "interp"):
        self.title = "Savitzky Golay"
        self.key = "sgolay"
        self.mode = mode
        if (window_size % 2) != 0:
            self.window_size = window_size
        else:
            raise Exception("Window size must be odd number!")
        if window_size > polynomial_order:
            self.polynomial_order = polynomial_order
        else:
            raise Exception("Window size must be higher than the polynomial order!")

    def apply(self, dataset, bands: list[str]):
        filtered_dataset = dataset.copy(deep=True)
        for band in bands:
            filtered_dataset[f'{band}_{self.key}'] = savgol_filter(
                filtered_dataset[band],
                window_length=self.window_size,
                polyorder=self.polynomial_order,
                mode=self.mode
            )
        return filtered_dataset

class Whittaker:
    """Whittaker–Eilers smoothing."""

    def __init__(self, lambda_: float, finite_diff: int = 2):
        self.title = "Whittaker–Eilers"
        self.key = "whitakker"
        self.lambda_ = lambda_
        self.finite_diff = finite_diff

    def smooth(self, array_data):
        y = np.asarray(array_data, dtype=float)
        m = len(y)

        # Identity matrix
        E = diags([1.0], [0], shape=(m, m), format="csc")

        # Difference operator
        diagonals = []
        offsets = []
        for i in range(self.finite_diff + 1):
            diagonals.append(((-1) ** i) * np.ones(m))
            offsets.append(i)

        D = diags(diagonals, offsets, shape=(m - self.finite_diff, m), format="csc")

        return spsolve(E + self.lambda_ * (D.T @ D), y)

    def apply(self, dataset, bands: list[str]):
        filtered_dataset = dataset.copy(deep=True)
        for band in bands:
            filtered_dataset[f'{band}_{self.key}'] = self.smooth(filtered_dataset[band])
        return filtered_dataset

class MovingAverage:
    """Centered Moving Average."""

    def __init__(self, window: int, min_periods: int, center: bool = True):
        self.title = "Centered Moving Average"
        self.key = "cma"
        self.window = window
        self.min_periods = min_periods
        self.center = center

    def apply(self, dataset, bands: list[str]):
        filtered_dataset = dataset.copy(deep=True)
        for band in bands:
            filtered_dataset[f'{band}_{self.key}'] = filtered_dataset[band].rolling(
                window=self.window, center=self.center, min_periods=self.min_periods
            ).mean().to_numpy()
        return filtered_dataset

class Gam:
    """Generalized Additive Model (GAM) Smoothing."""

    def __init__(self, n_splines: int, spline_order: int, feature: int = 0):
        self.title = "Generalized Additive Model (GAM)"
        self.key = "gam"
        self.n_splines = n_splines
        self.spline_order = spline_order
        self.feature = feature
        self.time_index_2d = None

    def GAM(self, array_data):
        time_index_2d = np.arange(len(array_data))[:, None]
        gam = LinearGAM(
            s(self.feature, n_splines=self.n_splines, spline_order=self.spline_order)
        ).fit(time_index_2d, array_data)
        return gam.predict(time_index_2d)

    def apply(self, dataset, bands: list[str]):
        filtered_dataset = dataset.copy(deep=True)
        for band in bands:
            filtered_dataset[f'{band}_{self.key}'] = self.GAM(filtered_dataset[band])
        return filtered_dataset

options = {
    "Savitzky Golay": SGolay,
    "Whittaker–Eilers": Whittaker,
    "Centered Moving Average": MovingAverage,
    "Generalized Additive Model (GAM)": Gam
}

class SmoothingFilter:
    """Smoothing filters helper."""

    def __init__(self, dataset):
        self.dataset = dataset.copy(deep=True)
        self.options = options
        self.selected_option = SGolay(19, 3)

    def select(self, selection):
        instance_ = 0
        for option in list(self.options.keys()):
            if isinstance(selection, self.options[option]):
                self.selected_option = selection
                instance_ += 1
        if not instance_:
            raise Exception(f"Selection is not an instance of any filter in {self.options}!")

    def apply(self, bands: list[str]):
        self.dataset = self.selected_option.apply(self.dataset, bands)

    def getBands(self):
        time_key = "Index"
        all_ = list(self.dataset.keys())
        return all_[(all_.index(time_key) + 1):len(all_)]

    def plot(self, title: str, select_band: str = None, original: bool = True):
        fig = plt.figure(figsize = (12, 5))
        fig.suptitle(title)
        seaborn.set_theme(style="darkgrid")
        bands_ = self.getBands()
        if select_band:
           bands_ = [band for band in bands_ if select_band in band]
        for band in bands_:
            if self.selected_option.key in band:
                label_ = band.replace(f"_{self.selected_option.key}", f" {self.selected_option.title}")
                seaborn.lineplot(
                    data = self.dataset,
                    x = "Index", y = band, label = label_,
                    markersize = 8, linestyle = '-', picker = 10
                )
            elif original:
                seaborn.lineplot(
                    data = self.dataset,
                    x = "Index", y = band, label = band,
                    markersize = 8, marker = 'o',
                    linestyle = '-', picker = 10,
                    color="grey", alpha=0.5
                )
        fig.canvas.mpl_connect('pick_event', get_source_from_click)
        fig.autofmt_xdate()
        plt.xlabel(None)
        plt.ylabel(None)
        plt.legend(
            bbox_to_anchor=(1.01, 1),
            loc='upper left',
            borderaxespad=0
        )
        plt.show()
