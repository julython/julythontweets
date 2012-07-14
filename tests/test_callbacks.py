"""Test generic callbacks for twitter, etc."""

import json
from tornado.simple_httpclient import SimpleAsyncHTTPClient
from unittest2 import TestCase

from julythontweets import callbacks
from julythontweets import config

_ORIGINAL_FETCH = SimpleAsyncHTTPClient.fetch
_ORIGINAL_LIVE_URL = config.JULYTHON_LIVE_ENDPOINT_URL

class TestCallbacks(TestCase):

    def tearDown(self):
        SimpleAsyncHTTPClient.fetch = _ORIGINAL_FETCH
        config.JULYTHON_LIVE_ENDPOINT_URL = _ORIGINAL_LIVE_URL

    def test_julython_live_twitter_callback(self):
        results = {}
        def fake_fetch(client, url, callback, method, body):
            results["method"] = method
            results["body"] = body
            results["url"] = url

        SimpleAsyncHTTPClient.fetch = fake_fetch
        config.JULYTHON_LIVE_ENDPOINT_URL = "http://localhost/api/v1/live"

        normalized_tweet = {
            "message": "Awesome!",
            "username": "joshmarshall",
            "picture_url": "http://stuff.com/whatever.jpg"
        }
        callback = callbacks.JulythonLiveTwitterCallback(None)
        callback(normalized_tweet)
        self.assertEqual(results["method"], "POST")
        self.assertEqual(results["url"], "http://localhost/api/v1/live")
        self.assertEqual(normalized_tweet, json.loads(results["body"]))

