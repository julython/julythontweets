"""The basic watcher interface."""

class Watcher(object):
    """Just the basic interface for IOLoop watchers."""

    def __init__(self, ioloop, callback, configuration):
        """The configuration should be a dict of whatever is needed."""
        self._ioloop = ioloop
        self._configuration = configuration
        self._callback = callback

    def start(self):
        """
        Do whatever is necessary to attach to the IOLoop, but 
        don't actually start the IOLoop yourself.
        
        """
        raise NotImplementedError("All watchers must implement a start() "
            "method.")
