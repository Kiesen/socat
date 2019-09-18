# -*- coding: utf-8 -*-
"""
Config file contains default configuratuion for
the CountVectorizer, LDA, K-Means and also the
logfile plotting.

To overwrite config create an config_local.py file.

"""

# Number of top words, that should be printed out
NO_TOP_WORDS = 4
NO_TOPICS = 8

# Logfile plotting configuration
PLOT_CONF = {
    "title": "Ø Zeit zum Empfangen von 1.000 Tweets",
    "legend_avg": "Ø sieben Tage = ",
    "legend_bar": "Ø am Tag",
    "output_title": "data-ttr",
    "output_type": ".pdf",
    "time_unit": "m",
    "ylabel": "Zeit in Minuten",
    "xlabel": "",
    "range_from": 0,
    "range_to": 7
}

# TF default configuration
TF_CONF = {
    "max_features": 1000,
    "max_df": 0.4,
    "min_df": 15
}

# LDA default configuration
LDA_CONF = {
    "learning_method": "online",
    "topic_word_prior": 1 / NO_TOPICS,
    "doc_topic_prior": 1 / NO_TOPICS,
    "max_iter": 5
}

KMEANS_CONF = {}

# Try to import local settings which can be used to override any of the above
try:
    from analyze.config_local import *
except ImportError:
    pass
