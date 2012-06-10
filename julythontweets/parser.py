"""The interface for parsing messages from Twitter, etc."""

class Parser(object):
    """ Just the basic interface for parsers."""

    def __init__(self, ioloop, configuration):
        """The configuration should be a dict of whatever you want, really."""
        self._configuration = configuration
        self._ioloop = ioloop

    def parse(self, message, callback):
        """All parsers should expect a string message and a callback."""
        raise NotImplementedError("All Parsers must implement "
            "'parse(self, message, callback)'.")

