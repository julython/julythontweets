"""Test that a tweet event hits the (fake) Julython API."""

import json
from tests.helpers import TimeoutMixin
from tornado.testing import AsyncHTTPTestCase
from tornado.web import RequestHandler, Application

from julythontweets import config
from julythontweets.watcher_registry import register_watchers
from julythontweets.watchers.twitter_watcher import TwitterWatcher

class FakeLiveHandler(RequestHandler):
    pass

_ORIGINAL_START = TwitterWatcher.start
_ORIGINAL_LIVE_URL = config.JULYTHON_LIVE_ENDPOINT_URL

class TestLiveTweets(AsyncHTTPTestCase, TimeoutMixin):

    def setUp(self):
        super(TestLiveTweets, self).setUp()
        self._ioloop = self.io_loop

    def tearDown(self):
        super(TestLiveTweets, self).tearDown()
        TwitterWatcher.start = _ORIGINAL_START
        config.JULYTHON_LIVE_ENDPOINT_URL = _ORIGINAL_LIVE_URL

    def get_app(self):
        return Application([
            ("/api/v1/live", FakeLiveHandler)
        ])

    def get_http_port(self):
        port = super(TestLiveTweets, self).get_http_port()
        config.JULYTHON_LIVE_ENDPOINT_URL = \
            "http://127.0.0.1:%d/api/v1/live" % port
        return port

    def test_new_tweet(self):

        # overwriting TwitterWatcher.start so it doesn't actually
        # connect to twitter, just throws a new tweet on the stack.
        def fake_start(watcher):
            def send_tweet():
                watcher.extract_from_tweet({
                    "text": "Awesome!",
                    "user": {
                        "screen_name": "joshmarshall",
                        "profile_image_url": "http://stuff.com/profile.jpg"
                    }
                })
            self.io_loop.add_callback(send_tweet)

        result = {}
        def fake_post(handler):
            result["body"] = handler.request.body
            self.io_loop.stop()
        FakeLiveHandler.post = fake_post

        TwitterWatcher.start = fake_start
        register_watchers(self.io_loop)
        self.add_timeout(1)
        self.io_loop.start()
        # blocks until timeout or callback
        result = json.loads(result["body"])
        self.assertEqual({
            "message": "Awesome!",
            "username": "joshmarshall",
            "picture_url": "http://stuff.com/profile.jpg"
        }, result)
