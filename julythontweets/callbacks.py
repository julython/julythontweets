"""Generic callbacks for various watchers."""

import logging
import json
from tornado.httpclient import AsyncHTTPClient

from julythontweets import config

class JulythonLiveTwitterCallback(object):

    def __init__(self, ioloop):
        self._ioloop = ioloop

    def __call__(self, tweet):
        client = AsyncHTTPClient(io_loop=self._ioloop)
        client.fetch(
            config.JULYTHON_LIVE_ENDPOINT_URL,
            method="POST", body=json.dumps(tweet),
            callback=self._request_callback)

    def _request_callback(self, response):
        if response.code != 201:
            logging.error(
                "Could not request live API (%s): %s", response.code,
                response.body)

