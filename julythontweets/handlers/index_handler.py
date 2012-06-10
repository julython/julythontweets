"""The (does nothing for now) IndexHandler."""

from tornado.web import RequestHandler

class IndexHandler(RequestHandler):

    def get(self):
        self.write({
            "status": "ok"
        })
