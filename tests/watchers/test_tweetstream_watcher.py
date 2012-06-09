"""Test the Twitter watcher."""

from julythontweets.watchers.twitter_watcher import TwitterWatcher
from julythontweets.watchers.twitter_watcher import MissingTwitterConfiguration

import time
from tornado.ioloop import IOLoop
from tweetstream import TweetStream
from unittest2 import TestCase

# Since we're going to be "catching" this call,
# we need to save it and reset it after the test is done
_ORIGINAL_TWEETSTREAM_FETCH = TweetStream.fetch

class TestTwitterWatcher(TestCase):

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

    def add_timeout(self, seconds):
        """Just add a timeout to the IOLoop."""
        self._ioloop.add_timeout(time.time() + seconds, self._ioloop_timeout)

    def _ioloop_timeout(self):
        """The callback(s) weren't called properly."""
        self._ioloop.stop()
        self.fail("The IOLoop timed out.")

    def test_twitter_watcher(self):

        def callback(result):
            self.fail("Callback should not have been called.")

        config = {
            "twitter_username": "whatever",
            "twitter_password": "foobar",
            "twitter_search_term": "searching",
            "parsers": {}
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
            self._ioloop.stop()

        parsers = {
            "www.google.com": FakeParser()
        }
        config = {
            "twitter_username": "who",
            "twitter_password": "whowho",
            "twitter_search_term": "ireallywanttoknow",
            "parsers": parsers
        }
        # should do a full redirect on this
        original_url = "http://bit.ly/julythongoogle"
        final_url = "http://www.google.com/search?q=julython"
        twitter_watcher = TwitterWatcher(self._ioloop, callback, config)
        twitter_watcher.extract_from_tweet({
            "text": "This is an awesome tweet! %s" % original_url,
            "name": "Josh Marshall"
        })
        self.add_timeout(5)
        self._ioloop.start()
        self.assertEqual(final_url, result["message"])
