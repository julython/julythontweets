"""
Imports all the handlers and registers them to a router with
register_handlers

"""

from julythontweets.handlers.index_handler import IndexHandler

def register_handlers(router):
    """Add handlers to the router."""
    router.add_route("/", IndexHandler, "index")
