"""The (uber simple) router for Tornado hooks."""

class MissingRoute(Exception):
    """Raised when a specific route cannot be found."""
    pass

class Router(object):
    """Holds the routes for tornado."""

    def __init__(self):
        self._routes = []

    def add_route(self, route, handler, name):
        """Store a route with the existing routes."""
        self._routes.append({
            "route": r"%s" % route,
            "handler": handler,
            "name": name
        })

    def get_routes(self):
        """Return a Tornado Application compatible list of routes."""
        routes = []
        for route in self._routes:
            routes.append((route["route"], route["handler"]))
        return routes

    def remove_route(self, name):
        """Remove a route by name."""
        to_remove = None
        for route in self._routes:
            if route["name"] == name:
                to_remove = route
                break
        if not to_remove:
            raise MissingRoute("Could not find route named '%s'" % name)
