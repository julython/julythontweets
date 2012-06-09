"""Test the config object."""

from julythontweets import config

import os
from unittest2 import TestCase

class TestConfig(TestCase):

    def setUp(self):
        self._environ_defaults = os.environ.copy()

    def tearDown(self):
        for key, value in self._environ_defaults.iteritems():
            if os.environ[key] != value:
                os.environ[key] = value

    def test_config_defaults(self):
        self.assertEqual(config.PORT, 9000)
        self.assertEqual(config.HOST, "localhost")
        self.assertEqual(config.JULYTHON_ENDPOINT_URL,
            "http://localhost:8080/api/v1/commits")
        self.assertEqual(config.JULYTHON_ENDPOINT_SECRET, "foobar")
        self.assertEqual(config.TWITTER_USERNAME, "faketwitter")
        self.assertEqual(config.TWITTER_PASSWORD, "fakepassword")

    def test_config_overwrite(self):
        os.environ["TWITTER_USERNAME"] = "newtwitter"
        os.environ["TWITTER_PASSWORD"] = "newpassword"
        os.environ["PORT"] = "7081"
        os.environ["JULYTHON_ENDPOINT_URL"] = "http://1.1.1.1:9999"
        reload(config)
        self.assertEqual(config.TWITTER_USERNAME, "newtwitter")
        self.assertEqual(config.TWITTER_PASSWORD, "newpassword")
        self.assertEqual(config.PORT, 7081)
        self.assertEqual(config.JULYTHON_ENDPOINT_URL, "http://1.1.1.1:9999")


