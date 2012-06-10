"""Takes a GitHub URL and extracts information about a commit, if possible."""

from julythontweets.parser import Parser


import logging
from HTMLParser import HTMLParser
from tornado.httpclient import AsyncHTTPClient
from xml.dom.minidom import parseString
from xml.parsers.expat import ExpatError

class GitHubParser(Parser):

    def __init__(self, ioloop, configuration):
        super(GitHubParser, self).__init__(ioloop, configuration)
        self._client = AsyncHTTPClient(io_loop=self._ioloop)

    def parse(self, url, callback):
        """Extract the information from a commit using GitHub's api."""
        # probably should abstract this into a class at some point
        def github_html_response(response):
            """Extract atom from HTML."""
            if response.code != 200:
                logging.warning("GitHub URL response invalid: %s",
                    response.code)
                return
            atom_link = get_commit_atom_link(response.body)
            self._client.fetch(atom_link, callback=github_commit_response)

        def github_commit_response(response):
            """Extract most recent commit from an Atom feed."""
            if response.code != 200:
                logging.warning("GitHub Atom URL response invalid: %s",
                    response.code)
            commit = get_most_recent_commit(response.body)
            callback(commit)

        self._client.fetch(url, callback=github_html_response)


class MissingAtomLink(Exception):
    """Raised when Atom link is not found in HTML."""
    pass


class GitHubAtomHTMLParser(HTMLParser):

    def set_atom_link_callback(self, callback):
        """Sets the callback for any atom links that are found."""
        self._link_callback = callback

    def handle_starttag(self, tag, attributes):
        """Look for a <link> element."""
        if tag != "link":
            return
        attributes = dict(attributes)
        if attributes.get("type") != "application/atom+xml":
            return
        # bleeechhh...
        if "commits" not in attributes.get("title", "").lower():
            return
        if "href" not in attributes:
            logging.warning("Missing HREF attribute in link element?")
        self._link_callback(attributes["href"])


def get_commit_atom_link(html):
    """Extract atom link (if possible) from HTML page."""
    atom_links = []
    def atom_link_callback(url):
        atom_links.append(url)
    parser = GitHubAtomHTMLParser()
    parser.set_atom_link_callback(atom_link_callback)
    parser.feed(html)
    if not atom_links:
        raise MissingAtomLink("No Atom links found in HTML.")
    if len(atom_links) > 1:
        logging.warning("Found %d atom links -- grabbing the first.",
            len(atom_links))
    atom_link = atom_links[0]
    return atom_link


class MissingCommit(Exception):
    """Raised when a commit cannot be found in an Atom feed."""
    pass


def _get_text(element):
    text_values = []
    for child_node in element.childNodes:
        if child_node.nodeType == child_node.TEXT_NODE:
            text_values.append(child_node.data.strip())
    return " ".join(text_values)


class GitHubAtomFeed(object):
    """Extracts information from a GitHub Atom feed of commits."""
    
    def __init__(self, feed):
        self._feed = feed

    def _get_dom(self):
        if not hasattr(self, "_dom"):
            self._dom = parseString(self._feed)
        return self._dom

    def get_commits(self):
        """Extract commits, most recent first, from feed."""
        try:
            dom = self._get_dom()
        except ExpatError, exc:
            raise MissingCommit("Could not parse Atom feed: %s" % exc)
        entries = dom.getElementsByTagName("entry")
        commits = []
        for entry in entries:
            commit = GitHubCommit(self, entry)
            commits.append(commit)
        return commits

    def get_project_id(self):
        """Get project id from feed."""
        dom = self._get_dom()
        id_element = dom.getElementsByTagName("id")[0]
        id_string = _get_text(id_element)
        # man, this is shaky...
        service_id = id_string.split("2008:/")[1].split("/commits")[0]
        return service_id


class GitHubCommit(object):

    def __init__(self, atom_feed, entry):
        self._atom_feed = atom_feed
        self._entry = entry
        self._title = self._parse_title()
        self._commit = self._parse_commit()
        self._author = self._parse_author()
        self._project = self._atom_feed.get_project_id()


    def _parse_title(self):
        title_element = self._entry.getElementsByTagName("title")[0]
        return _get_text(title_element)

    def _parse_commit(self):
        id_element = self._entry.getElementsByTagName("id")[0]
        commit_id_string = _get_text(id_element)
        commit_id_parts = commit_id_string.split(",")
        # this feels nyasty..
        commit_id = commit_id_parts[1].split("/")[1]
        return commit_id

    def _parse_author(self):
        author_element = self._entry.getElementsByTagName("author")[0]
        name_element = author_element.getElementsByTagName("name")[0]
        uri_element = author_element.getElementsByTagName("uri")[0]
        name = _get_text(name_element)
        uri = _get_text(uri_element)
        username = uri.split("/")[-1]
        return GitHubAuthor(name=name, url=uri, username=username)

        


    def to_dict(self):
        return {
            "commit": self._commit,
            "author": self._author.to_dict(),
            "title": self._title,
            "project": {
                "service": "github",
                "id": self._project
            }
        }


class GitHubAuthor(object):

    def __init__(self, name, url, username):
        self._name = name
        self._url = url
        self._username = username
        self._service = "github"

    def to_dict(self):
        return {
            "name": self._name,
            "username": self._username,
            "url": self._url,
            "service": self._service
        }


def get_most_recent_commit(feed):
    """Extract a commit (if possible) from Atom XML."""
    atom_feed = GitHubAtomFeed(feed)
    commits = atom_feed.get_commits()
    if not commits:
        raise MissingCommit("No commits were found in Atom feed.")
    # grabbing first one, assuming it's the most recent for now
    commit = commits[0]
    return commit.to_dict()
