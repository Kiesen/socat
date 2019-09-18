import os
import unittest
from stream.tweet_streamer import TweetStreamer


class TestTweetStreamer(unittest.TestCase):

    def test__init__(self):
        stream_instance = TweetStreamer()
        self.assertEqual(
            stream_instance._api._access_token_secret,
            os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        )
        self.assertEqual(
            stream_instance._api._access_token_key,
            os.getenv("TWITTER_ACCESS_TOKEN")
        )
        self.assertEqual(
            stream_instance._api._consumer_secret,
            os.getenv("TWITTER_CONSUMER_SECRET")
        )
        self.assertEqual(
            stream_instance._api._consumer_key,
            os.getenv("TWITTER_CONSUMER_KEY")
        )
        self.assertEqual(stream_instance._ret_max, 100)
        self.assertEqual(stream_instance._ver, False)
        self.assertEqual(stream_instance._log, False)


if __name__ == "__main__":
    unittest.main()
