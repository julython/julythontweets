"""Test the watcher registration."""

from julythontweets.watchers.twitter_watcher import TwitterWatcher
from julythontweets.watcher_registry import register_watchers
from julythontweets.watcher_registry import get_watcher_configuration

from unittest2 import TestCase

_TWITTER_WATCHER_START = TwitterWatcher.start

class FakeIOLoop(object):
    pass


class TestWatcherRegistry(TestCase):

    def tearDown(self):
        TwitterWatcher.start = _TWITTER_WATCHER_START

    def test_get_watcher_configuration(self):
        ioloop = FakeIOLoop()
        twitter_config = get_watcher_configuration("twitter", ioloop)
        self.assertEqual(
            "fakeconsumerkey", twitter_config["twitter_consumer_key"])
        self.assertEqual(
            "fakeconsumersecret", twitter_config["twitter_consumer_secret"])
        self.assertEqual(
            "fakeaccesstoken", twitter_config["twitter_access_token"])
        self.assertEqual(
            "fakeaccesstokensecret",
            twitter_config["twitter_access_token_secret"])
        self.assertEqual("julython", twitter_config["twitter_search_term"])
        self.assertTrue("github.com" in twitter_config["parsers"])
        self.assertTrue("www.github.com" in twitter_config["parsers"])

    def test_register_watchers(self):
        # there's gotta be a way to make this less intrusive
        result = {}
        def twitter_start(watcher):
            result["twitter_called"] = True
        TwitterWatcher.start = twitter_start
        ioloop = FakeIOLoop()
        register_watchers(ioloop)
        self.assertTrue(result["twitter_called"])

