"""Classes for interacting with Julython."""

import json
import urllib

from tornado.httpclient import AsyncHTTPClient


class FailedToSave(Exception):
    """Raised when a bad response code is returned from a save operation."""
    pass

class Connection(object):
    """Just a wrapper for AsyncHTTPClient that keeps configuration."""

    def __init__(self, ioloop, url):
        self._url = url
        self._ioloop = ioloop

    def get_client(self):
        if not hasattr(self, "_client"):
            self._client = AsyncHTTPClient(io_loop=self._ioloop)
        return self._client

    def fetch(self, path, callback, *args, **kwargs):
        client = self.get_client()
        separator = ""
        if not self._url.endswith("/") and not path.endswith("/"):
            separator = "/"
        path = self._url + separator + path
        # update headers here when necessary with key, etc.
        client.fetch(
            path, *args, callback=callback, **kwargs)


class Project(object):

    def __init__(self, connection, project_id, body):
        self._connection = connection
        self._project_id = urllib.quote_plus(project_id)
        self._body = body

    def to_url(self):
        return "projects/%s" % self._project_id

    def to_json(self):
        return json.dumps(self._body)

    def save(self, callback):
        """Check if it already exists, save it if not."""
        def check_callback(response):
            if response.code != 404:
                # eventually, we'll support updating a project?
                return callback(self)
            self._connection.fetch(
                self.to_url(), method="POST", body=self.to_json(),
                callback=save_callback)

        def save_callback(response):
            if response.code != 201:
                raise FailedToSave(
                    "Could not save project (%d): %s" % 
                    (response.code, response.body))
            callback(self)

        self._connection.fetch(
            self.to_url(), method="GET", callback=check_callback)
