"""Test IOLoop watcher interface."""

from julythontweets.watcher import Watcher

from tornado.ioloop import IOLoop

from unittest2 import TestCase

class TestWatcher(TestCase):

    def test_base_watcher(self):
        """Test the watcher interface."""
        ioloop = IOLoop()
        def callback():
            pass
        watcher = Watcher(ioloop, callback, {})
        with self.assertRaises(NotImplementedError):
            watcher.start()
