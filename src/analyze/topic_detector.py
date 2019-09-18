# -*- coding: utf-8 -*-
"""
Module for topic detection.

Uses the utils module for reading in data from a given path.
Also uses the text extraction feature, lda and kmeans from sklearn.

"""
import os
import pandas as pd
from time import time
from langdetect import detect
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import TruncatedSVD, LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

from analyze import utils
from analyze.config import TF_CONF, LDA_CONF, NO_TOP_WORDS, NO_TOPICS


class TopicDetector():

    def __init__(self, path=None, methode=None, lang=None):
        """
        Set initially all important properties to the
        topic detector instance.

        Convert the returned dataframe to a series object,
        because at the moment we only want to look at the text entry.
        After that step filter the series object .
        """
        self._methode = methode
        self._s = utils.create_df_from_path(path, 'data')['text']

        # If entries should be pre filtered by language
        if(lang):
            self._s = self._filter_language(s=self._s, lang=lang)

        # Try to read in a list of stop words
        try:
            with open('./analyze/stopwords-ger.txt') as f:
                self._stop_words = f.read().splitlines()
        # If an error is thrown it is likely a FileNotFoundError
        except Exception:
            self._stop_words = None
            pass

    def start(self):
        # Start the topic detection process.
        if self._methode == 'LDA':
            self._lda()
        elif self._methode == 'KM':
            self._km()
        else:
            self._lda()
            self._km()

    def _filter_language(self, s=None, lang='de'):
        # Print info
        print("\nFilter entries by language")
        print("----------------------------------------------------\n")
        print("The filtering process can take some time to complete!")
        print("For 20k entries about 2-3 Minutes.")
        print("Start filtering...")

        # Helper function for language filtering
        def lang_helper(entry):
            if type(entry) is str:
                try:
                    return detect(entry) == lang
                except Exception:
                    return False
            return False

        if(s is not None):
            # Measure time it takes to fit lda
            t = time()
            try:
                s = s[s.apply(lambda x: lang_helper(x))]
            except Exception:
                pass

            # Print info
            print("Done in %0.2f secounds\n\n" % (time() - t))
            return s

    def _lda(self):
        # Print info
        print("\nTopic detection with the use of LDA")
        print("----------------------------------------------------\n")
        print("Create the document term matrix")

        # Measure time it takes to fit lda
        t = time()

        # Create the vocabulary. Used for LDA and k-means
        vectorizer = CountVectorizer(
            stop_words=self._stop_words,
            max_features=TF_CONF["max_features"],
            max_df=TF_CONF["max_df"],
            min_df=TF_CONF["min_df"]
        )
        tf = vectorizer.fit_transform((self._s).values.astype('U'))
        feature_names = vectorizer.get_feature_names()

        # Print info
        print("Done in %0.2f secounds" % (time() - t))
        print("Number of used stop words: %d" % len(self._stop_words))
        print("Number of entries: %d, words: %d \n" % tf.shape)
        print("Start fitting LDA...")

        # Initialize LDA and fit it with the created vocabulary
        lda = LatentDirichletAllocation(
            topic_word_prior=LDA_CONF["topic_word_prior"],
            doc_topic_prior=LDA_CONF["doc_topic_prior"],
            learning_method=LDA_CONF["learning_method"],
            max_iter=LDA_CONF["max_iter"],
            n_components=NO_TOPICS,
            random_state=0
        ).fit(tf)

        # Print info
        print("Done in %0.2f secounds" % (time() - t))
        print("Predicted topics:")

        # Print out the result
        for topic_idx, topic in enumerate(lda.components_):
            print("Topic mixture %d: " % (topic_idx), end="")
            print(" ".join(
                [feature_names[i] for i in topic.argsort()
                    [:-NO_TOP_WORDS - 1:-1]])
            )

        print("\n")

    def _km(self):
        # Print info
        print("\nTopic detection with the use of k-means")
        print("----------------------------------------------------\n")
        print("Create the document term matrix...")

        # Measure time it takes to fit km
        t = time()

        # Create the vocabulary. Used for LDA and k-means
        vectorizer = TfidfVectorizer(
            stop_words=self._stop_words,
            max_features=TF_CONF["max_features"],
            max_df=TF_CONF["max_df"],
            min_df=TF_CONF["min_df"]
        )
        tf = vectorizer.fit_transform((self._s).values.astype('U'))
        feature_names = vectorizer.get_feature_names()

        # Print info
        print("Done in %0.2f secounds" % (time() - t))
        print("Number of used stop words: %d" % len(self._stop_words))
        print("Number of entries: %d, words: %d \n" % tf.shape)
        print("Start fitting k-means...")

        svd = TruncatedSVD(NO_TOPICS)
        normalizer = Normalizer(copy=False)
        lsa = make_pipeline(svd, normalizer)
        tf_lsa = lsa.fit_transform(tf)

        # Initialize k-means and fit it with the created vocabulary
        km = KMeans(
            n_clusters=NO_TOPICS,
            random_state=0,
            n_init=1
        ).fit(tf_lsa)

        # Print info
        print("Done in %0.2f secounds" % (time() - t))
        print("Predicted topics:")

        original_space_centroids = svd.inverse_transform(km.cluster_centers_)
        order_centroids = original_space_centroids.argsort()[:, ::-1]

        for i in range(NO_TOPICS,):
            print("Cluster %d:" % i, end="")
            for ind in order_centroids[i, :NO_TOP_WORDS]:
                print(" %s" % feature_names[ind], end="")
            print()

        # End with two new lines
        print("\n")
