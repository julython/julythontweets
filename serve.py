"""Just the basic init script."""

from julythontweets import config
from julythontweets.application import Application
from julythontweets.handler_registry import register_handlers
from julythontweets.watcher_registry import register_watchers
from julythontweets.router import Router

from tornado.ioloop import IOLoop

def main():
    ioloop = IOLoop.instance()
    router = Router()
    register_handlers(router)
    app = Application(router.get_routes())
    app.listen(config.port, io_loop=ioloop)
    register_watchers(ioloop)
    ioloop.start()

if __name__ == "__main__":
    main()
