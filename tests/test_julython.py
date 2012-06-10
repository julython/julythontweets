"""Test the Julython API library."""

from julythontweets import config
from julythontweets.julython import Connection, Project
#User, Commit

import json
import time
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application, RequestHandler, HTTPError

# Building out the fake API. Contract driven! :)

FAKE_DB = {
    "projects": {},
    "users": {}
}

def clear_db():
    FAKE_DB["projects"] = {}
    FAKE_DB["users"] = {}

class FakeProjectHandler(RequestHandler):
    def get(self, project_id):
        if project_id not in FAKE_DB["projects"]:
            raise HTTPError(404)
        self.write(FAKE_DB["projects"][project_id])

    def post(self, project_id):
        body = json.loads(self.request.body)
        if project_id in FAKE_DB["projects"]:
            raise HTTPError(400)
        body["commits"] = []
        body["users"] = []
        FAKE_DB["projects"][project_id] = body
        self.set_status(201)
        self.write(body)

class FakeUserHandler(RequestHandler):
    def get(self, user_id):
        if user_id not in FAKE_DB["users"]:
            raise HTTPError(404)
        self.write(FAKE_DB["users"][user_id])

    def post(self, user_id):
        body = json.loads(self.request.body)
        if user_id in FAKE_DB["users"]:
            raise HTTPError(400)
        FAKE_DB["users"][user_id] = body
        self.set_status(201)
        self.write(body)

class FakeCommitsHandler(RequestHandler):
    def post(self, project_id):
        body = json.loads(self.request.body)
        user_id = body["user_id"]
        project = FAKE_DB["projects"][project_id]
        if user_id not in project["users"]:
            project["users"].append(user_id)
        project["commits"].append(body)
        self.set_status(201)
        self.write(body)

class TestJulython(AsyncHTTPTestCase):

    def tearDown(self):
        super(TestJulython, self).tearDown()
        clear_db()

    def get_app(self):
        return Application([
            ("/api/v1/projects/([^/]+)", FakeProjectHandler),
            ("/api/v1/projects/([^/]+)/commits", FakeCommitsHandler),
            ("/api/v1/users/([^/]+)", FakeUserHandler)
        ])

    def test_julython_project(self):
        base_url = "http://localhost:%d/api/v1" % self.get_http_port()
        connection = Connection(self.io_loop, base_url)
        project = Project(
            connection, "github:julython/julythontweets",
            {
                "name": "julythontweets",
                "url": "https://github.com/julython/julythontweets",
            })
        def callback(project):
            self.stop()

        project_id = "github:julython/julythontweets"
        escaped_project_id = "github%3Ajulython%2Fjulythontweets"
        self.assertEqual("projects/%s" % escaped_project_id, project.to_url())
        project.save(callback)
        # blocks till stop or timeout
        self.wait()
        self.assertTrue(project_id in FAKE_DB["projects"])
        self.assertEqual(
            "julythontweets", FAKE_DB["projects"][project_id]["name"])



