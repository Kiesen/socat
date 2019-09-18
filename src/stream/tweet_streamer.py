# -*- coding: utf-8 -*-
"""
Module for streaming and saving tweets.

Loads the required credentials and opens the stream afterwards.
Use the utils module for I/O.
"""
import twitter
import time
import os

from dotenv import load_dotenv
from datetime import datetime, timedelta

from stream.config import TWITTER
from stream import utils


class TweetStreamer():

    def __init__(self, ret_max=100, ver=False, log=False, path=None):
        """
        Set initially all important properties to the streaming instance.
        Also create twitter api object.
        """
        load_dotenv()
        self._api = twitter.Api(
            os.getenv("TWITTER_CONSUMER_KEY"),
            os.getenv("TWITTER_CONSUMER_SECRET"),
            os.getenv("TWITTER_ACCESS_TOKEN"),
            os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        )

        self._ret_max = ret_max
        self._ver = ver
        self._log = log

        self._locations = TWITTER["locations"]
        self._languages = TWITTER["languages"]
        self._track = TWITTER["track"]

        self._data_dir = utils.set_output_path(path, '/data')
        self._log_dir = utils.set_output_path(path, '/logs')

    def start_streaming(self):
        try:
            # Set initial values for streaming
            recived_tweets = 0
            start_time = time.time()
            time_hash = datetime.now().strftime("%Y%m%d%H%M%S")
            log_date = datetime.now().strftime("%Y-%m-%-d")
            data_path = self._data_dir + "/twitter" + time_hash + ".json"
            log_path = self._log_dir + '/' + time_hash + '.log.json'

            # Requst on the stream endpoint of the twitter api
            stream = self._api.GetStreamFilter(
                locations=[self._locations],
                languages=[self._languages],
                track=[self._track]
            )

            # Add an empty list to the file
            utils.data_to_json(data_path, [])

            # Print inital info message and additonal info if verbose mode
            utils.print_initial_info(data_path)
            if(self._ver):
                utils.print_info(recived_tweets)

            # Write each tweet to the file and prompt additional information
            for tweet in stream:
                # First read the data and append it back to the json file
                data = utils.data_from_json(data_path)
                data.append(tweet)
                utils.data_to_json(data_path, data)

                # Increment tweet count
                recived_tweets += 1

                # If verbose mode active write info to stdout
                if self._ver:
                    utils.print_info(recived_tweets)

                # Check if the amount of recived tweets is reached
                if(recived_tweets >= self._ret_max):
                    stream.close()
                    elapsed_time = timedelta(
                        seconds=round((time.time() - start_time))
                    )
                    utils.print_summary(elapsed_time, recived_tweets)
                    if(self._log):
                        utils.data_to_json(
                            log_path,
                            self._params_to_json(
                                elapsed_time, 
                                recived_tweets,
                                log_date
                            )
                        )
                    return

        except Exception:
            """
            In case of an keyboard interrupt or in case of any other exception
            close the stream, print the summary and a log if requested.
            """
            stream.close()
            elapsed_time = timedelta(
                seconds=round((time.time() - start_time))
            )
            utils.print_summary(elapsed_time, recived_tweets)
            if(self._log):
                utils.data_to_json(
                    log_path,
                    self._params_to_json(
                        elapsed_time,
                        recived_tweets, log_date
                    )
                )

    def _params_to_json(self, elapsed_time, recived_tweets, datetime_now):
        """
        This function converts the given arguments to
        an valid json object, which is needed for the log files.

        return:
        json object -- a json object with log informations.
        """
        return ({
            "elapsed_time": str(elapsed_time),
            "recived_entries": str(recived_tweets),
            "date": str(datetime_now),
            "filter_parameter": {
                "locations": str(self._locations),
                "languages": str(self._languages),
                "track": str(self._track),
            }
        })
