"""Test the parser for messages."""

from julythontweets.parser import Parser

from unittest2 import TestCase

class TestParser(TestCase):

    def test_base_parser(self):
        """Test the parser interface."""
        parser = Parser({})
        def callback(result):
            raise Exception("This should not have been called")

        with self.assertRaises(NotImplementedError):
            parser.parse("This is teh message!", callback)
