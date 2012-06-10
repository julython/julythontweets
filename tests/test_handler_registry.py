"""Simple tests for the handler registry."""

from julythontweets.handler_registry import register_handlers
from unittest2 import TestCase

class FakeRouter(list):

    def add_route(self, route, handler, name):
        # trying not to test to death...
        self.append(name)


class TestHandlerRegistry(TestCase):

    def test_register_handlers(self):
        router = FakeRouter()
        register_handlers(router)
        self.assertTrue("index" in router)

