from julythontweets.application import Application
from julythontweets.router import Router

from tornado.testing import AsyncHTTPTestCase
from tornado.web import RequestHandler

class FakeHandler(RequestHandler):
    def get(self):
        self.write("WORKS!")

class TestApplication(AsyncHTTPTestCase):

    def get_router(self):
        if not hasattr(self, "_router"):
            self._router = Router()
            self._router.add_route("/", FakeHandler, "index")
        return self._router

    def clear_router(self):
        delattr(self, "_router")

    def get_app(self):
        return Application(self.get_router().get_routes())

    def test_app(self):
        response = self.fetch("/")
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "WORKS!")



