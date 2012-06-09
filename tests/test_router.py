"""Test the Router's functionality."""

from julythontweets.router import Router

from unittest2 import TestCase

class DumbHandler(object):
    pass

class TestRouter(TestCase):

    def test_router_construction(self):
        # should just work
        router = Router()
        self.assertIsNotNone(router)

    def test_router_add_route(self):
        router = Router()
        router.add_route("/", DumbHandler, "index")
        routes = router.get_routes()
        self.assertEqual(1, len(routes))
        self.assertEqual(2, len(routes[0]))
        self.assertEqual("/", routes[0][0])
        self.assertEqual(DumbHandler, routes[0][1])

    def test_router_remove_route(self):
        router = Router()
        router.add_route("/", DumbHandler, "index")
        router.remove_route("index")



