"""Test the basic index handler."""

from julythontweets.application import Application
from julythontweets.handlers.index_handler import IndexHandler
from julythontweets.router import Router

from tornado.testing import AsyncHTTPTestCase

class TestIndexHandler(AsyncHTTPTestCase):

    def get_app(self):
        router = Router()
        router.add_route("/", IndexHandler, "index")
        return Application(router.get_routes())

    def test_index_handler(self):
        response = self.fetch("/")
        self.assertEqual(200, response.code)
