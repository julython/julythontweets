"""Test the GitHub parser."""

from julythontweets.parsers.github_parser import GitHubParser
from julythontweets.parsers.github_parser import get_commit_atom_link
from julythontweets.parsers.github_parser import MissingAtomLink
from julythontweets.parsers.github_parser import get_most_recent_commit
from julythontweets.parsers.github_parser import MissingCommit

import os
from tests.helpers import TimeoutMixin
from tornado.ioloop import IOLoop
from unittest2 import TestCase

_TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), "../data")
_GITHUB_SAMPLE_HTML_PATH = os.path.join(_TEST_DATA_PATH,
    "github_sample_page.html")
_GITHUB_SAMPLE_ATOM_PATH = os.path.join(_TEST_DATA_PATH,
    "github_sample_atom.xml")

class TestGitHubParser(TestCase, TimeoutMixin):

    def setUp(self):
        self._ioloop = IOLoop()

    def test_github_parser(self):
        result = {}
        def callback(commit_result):
            for key in commit_result:
                result[key] = commit_result[key]
            self._ioloop.stop()

        github_parser = GitHubParser(self._ioloop, {})
        github_parser.parse("https://github.com/julython/"
            "julythontweets/commit/25645d2cf6b58d2657cf6eb0fb4ca59d5f2499f4",
            callback)

        self.add_timeout(3)
        self._ioloop.start()
        # will block until callback or timeout
        self.assertEqual("Josh Marshall",
            result["author"]["name"])
        self.assertEqual("joshmarshall",
            result["author"]["username"])
        self.assertEqual(
            "25645d2cf6b58d2657cf6eb0fb4ca59d5f2499f4",
            result["commit"])

    def test_get_commit_atom_link(self):
        """Test extracting commit Atom URL from an HTML page."""
        with self.assertRaises(MissingAtomLink):
            get_commit_atom_link("WHATEVER")
        with self.assertRaises(MissingAtomLink):
            get_commit_atom_link("<html></html>")
        html = open(_GITHUB_SAMPLE_HTML_PATH).read()
        atom_link = get_commit_atom_link(html)
        self.assertEqual(
            "https://github.com/julython/julythontweets/commits/master.atom",
            atom_link)

    def test_get_most_recent_commit(self):
        """Test extracting most recent commit from an Atom Feed."""
        with self.assertRaises(MissingCommit):
            get_most_recent_commit("whatever")
        with self.assertRaises(MissingCommit):
            get_most_recent_commit("<rss></rss>")
        feed = open(_GITHUB_SAMPLE_ATOM_PATH).read()
        commit = get_most_recent_commit(feed)
        self.assertEqual({
                "name": "Josh Marshall",
                "url": "https://github.com/joshmarshall",
                "username": "joshmarshall",
                "service": "github"
            }, commit["author"])
        self.assertEqual("25645d2cf6b58d2657cf6eb0fb4ca59d5f2499f4",
            commit["commit"])
        self.assertEqual("julython/julythontweets", commit["project"]["id"])
        self.assertEqual("github", commit["project"]["service"])
