"""Helpers / mixins for tests."""

import time

class TimeoutMixin(object):
    """Adds shortcuts for timeouts in a test."""

    def add_timeout(self, seconds):
        """Just add a timeout to the IOLoop."""
        self._ioloop.add_timeout(time.time() + seconds, self._ioloop_timeout)

    def _ioloop_timeout(self):
        """The callback(s) weren't called properly."""
        self._ioloop.stop()
        self.fail("The IOLoop timed out.")

