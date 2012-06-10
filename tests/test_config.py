"""Test the config object."""

from julythontweets import config

import os
from unittest2 import TestCase

_ENVIRON_DEFAULTS = os.environ.copy()

class TestConfig(TestCase):

    def setUp(self):
        self._environ_changed = {}

    def tearDown(self):
        for key, value in self._environ_changed.iteritems():
            if value is None:
                del os.environ[key]
            else:
                os.environ[key] = value
        reload(config)

    def _environ(self, key, value):
        self._environ_changed[key] = os.environ.get(key)
        os.environ[key] = value

    def test_config_defaults(self):
        self.assertEqual(config.PORT, 9000)
        self.assertEqual(config.HOST, "localhost")
        self.assertEqual(config.JULYTHON_ENDPOINT_URL,
            "http://localhost:8080/api/v1/commits")
        self.assertEqual(config.JULYTHON_ENDPOINT_SECRET, "foobar")
        self.assertEqual(config.TWITTER_CONSUMER_KEY, "fakeconsumerkey")
        self.assertEqual(config.TWITTER_CONSUMER_SECRET, "fakeconsumersecret")
        self.assertEqual(config.TWITTER_ACCESS_TOKEN, "fakeaccesstoken")
        self.assertEqual(
            config.TWITTER_ACCESS_TOKEN_SECRET, "fakeaccesstokensecret")
        self.assertEqual(config.TWITTER_SEARCH_TERM, "julython")

    def test_config_overwrite(self):
        self._environ("TWITTER_CONSUMER_KEY", "newkey")
        self._environ("TWITTER_CONSUMER_SECRET", "newsecret")
        self._environ("PORT", "7081")
        self._environ("JULYTHON_ENDPOINT_URL", "http://1.1.1.1:9999")
        reload(config)
        self.assertEqual(config.TWITTER_CONSUMER_KEY, "newkey")
        self.assertEqual(config.TWITTER_CONSUMER_SECRET, "newsecret")
        self.assertEqual(config.PORT, 7081)
        self.assertEqual(config.JULYTHON_ENDPOINT_URL, "http://1.1.1.1:9999")


