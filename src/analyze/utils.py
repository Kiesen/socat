# -*- coding: utf-8 -*-
"""
Utilities module of the analyze package.

Contains a function to create a dateframe from
a given path. Used in both, log_analyzer and topic_detector
modules.
"""

import os
import json
import pandas as pd


def create_df_from_path(path=None, dir_name='data'):
    """
    This function tries to read in json formatted files
    from a given path and saves them to da dataframe.

    return:
    dateframe -- a dataframe object.
    """
    df = pd.DataFrame()
    if path is None:
        path = os.getcwd() + '/' + dir_name

    if os.path.isdir(path):
        for file in os.listdir(path):
            try:
                with open(path + '/' + file) as f:
                    df = df.append(
                        pd.DataFrame.from_records(json.load(f)),
                        ignore_index=True,
                        sort=True
                    )
            except UnicodeDecodeError:
                pass
    return df
