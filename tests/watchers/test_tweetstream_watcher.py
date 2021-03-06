"""Test the Twitter watcher."""

from julythontweets.watchers.twitter_watcher import TwitterWatcher
from julythontweets.watchers.twitter_watcher import MissingTwitterConfiguration

from tests.helpers import TimeoutMixin
from tornado.ioloop import IOLoop
from tweetstream import TweetStream
from unittest2 import TestCase

# Since we're going to be "catching" this call,
# we need to save it and reset it after the test is done
_ORIGINAL_TWEETSTREAM_FETCH = TweetStream.fetch

class TestTwitterWatcher(TestCase, TimeoutMixin):

    def setUp(self):
        TweetStream.fetch = self._catch_tweetstream_fetch
        self._tweetstream_fetch_called = False
        self._ioloop = IOLoop()

    def tearDown(self):
        TweetStream.fetch = _ORIGINAL_TWEETSTREAM_FETCH

    def _catch_tweetstream_fetch(self, *args, **kwargs):
        """Just assert that this is called."""
        self._tweetstream_fetch_called = True
        self._ioloop.stop()

    def test_twitter_watcher(self):

        def callback(result):
            self.fail("Callback should not have been called.")

        config = {
            "twitter_consumer_key": "key",
            "twitter_consumer_secret": "secret",
            "twitter_access_token": "token",
            "twitter_access_token_secret": "token_secret",
            "twitter_search_term": "searching",
            "parsers": {},
            "callbacks": []
        }
        for key in config.keys():
            bad_config = config.copy()
            del bad_config[key]
            with self.assertRaises(MissingTwitterConfiguration):
                TwitterWatcher(self._ioloop, callback, bad_config)

        self.add_timeout(3)
        twitter_watcher = TwitterWatcher(self._ioloop, callback, config)
        twitter_watcher.start()
        self._ioloop.start()
        # blocks until the fetch callback or timeout
        self.assertTrue(self._tweetstream_fetch_called)

    def test_twitter_watcher_parse(self):
        class FakeParser(object):
            def __init__(self, *args, **kwargs):
                pass
            def parse(self, message, callback):
                callback({
                    "message": message
                })

        result = {}

        def callback(parsed_result):
            """When all is said and parsed, this gets called."""
            for key in parsed_result:
                result[key] = parsed_result[key]
            self.stop()

        parsers = {
            "www.google.com": FakeParser()
        }
        config = {
            "twitter_consumer_key": "key",
            "twitter_consumer_secret": "secret",
            "twitter_access_token": "token",
            "twitter_access_token_secret": "token_secret",
            "twitter_search_term": "ireallywanttoknow",
            "parsers": parsers,
            "callbacks": []
        }
        # should do a full redirect on this
        original_url = "http://bit.ly/julythongoogle"
        final_url = "http://www.google.com/search?q=julython"
        twitter_watcher = TwitterWatcher(self._ioloop, callback, config)
        twitter_watcher.extract_from_tweet({
            "text": "This is an awesome tweet! %s" % original_url,
            "user": {
                "name": "Josh Marshall",
                "screen_name": "joshmarshall",
                "profile_image_url": "http://stuff.com/profile.jpg"
            }
        })
        self.add_timeout(5)
        self._ioloop.start()
        self.assertEqual(final_url, result["message"])

    def test_twitter_callbacks(self):

        result = {}
        def fake_callback(tweet):
            result["tweet"] = tweet

        config = {
            "twitter_consumer_key": "key",
            "twitter_consumer_secret": "secret",
            "twitter_access_token": "token",
            "twitter_access_token_secret": "token_secret",
            "twitter_search_term": "whateverworks",
            "parsers": {},
            "callbacks": [fake_callback]
        }
        tweet = {
            "text": "This is a great tweet.",
            "user": {
                "screen_name": "joshmarshall",
                "profile_image_url": "http://stuff.com/profile.jpg"
            }
        }
        twitter_watcher = TwitterWatcher(self._ioloop, None, config)
        twitter_watcher.extract_from_tweet(tweet)
        self.assertEqual(result["tweet"], {
            "username": "joshmarshall",
            "message": "This is a great tweet.",
            "picture_url": "http://stuff.com/profile.jpg"
        })
