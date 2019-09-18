# -*- coding: utf-8 -*-
"""
Module for analyzing logfiles.

Uses the utils module for reading in the logfiles from a given path.
Also uses matplotlib for creating a bar plot from the logfiles.

"""

import pandas as pd
import numpy as np

# This is just a hacky way to use matplotlib in osx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from analyze import utils
from analyze.config import PLOT_CONF


class LogAnalyzer():

    def __init__(self, path=None, t_range=None):
        """
        Set initially all important properties to the
        log analyzer instance.
        """
        self._df = utils.create_df_from_path(path, 'logs')

        self._output_title = PLOT_CONF["output_title"]
        self._output_type = PLOT_CONF["output_type"]
        self._ylabel = PLOT_CONF["ylabel"]
        self._xlabel = PLOT_CONF["xlabel"]
        self._title = PLOT_CONF["title"]
        self._range_from = PLOT_CONF["range_from"]
        self._range_to = PLOT_CONF["range_to"]
        self._time_unit = PLOT_CONF["time_unit"]
        self._legend_avg = PLOT_CONF["legend_avg"]
        self._legend_bar = PLOT_CONF["legend_bar"]

    def create_bar_plot(self):
        """
        The create bar plot method firstly convertes the elapsed time entry
        to a valid timedelta64 secound type and then to an int64 used for
        calculation. Next group the df by date and calculate the mean
        elepased time per date, which will return a series object.
        Lastly convert the int64 back to a timedelta64 secound type and
        create the bar plot.
        """
        tmp_df = self._df
        if 'elapsed_time' in tmp_df and 'date' in tmp_df:
            tmp_df['elapsed_time'] = pd.to_timedelta(
                tmp_df['elapsed_time']
            ).astype('timedelta64[s]').astype(int)

            series = (
                tmp_df.groupby(tmp_df['date']).elapsed_time.mean()
            )[self._range_from:self._range_to]
            series = (
                (series.astype('timedelta64[s]')) /
                np.timedelta64(1, self._time_unit)
            )

            # Mean of the created series object
            mean = series.mean()

            # Create a bar plot from given dateframe
            _, ax = plt.subplots()
            series.plot(kind="bar", x=None, y=None, ax=ax, color="cornflowerblue")
            # Plot avg line
            ax.axhline(mean)

            # Set labels
            plt.legend(
                [
                    self._legend_avg + str(int(mean)),
                    self._legend_bar
                ]
            )
            plt.xlabel(self._xlabel)
            plt.ylabel(self._ylabel)
            plt.title(self._title)

            # Save to output file
            plt.gcf().autofmt_xdate()
            plt.savefig(self._output_title + self._output_type)
            print(
                '\n'
                + 'Created plot and saved it: '
                + self._output_title + self._output_type
                + '\n'
            )
        else:
            print('socat.py analyze: error: logs are not valid')
