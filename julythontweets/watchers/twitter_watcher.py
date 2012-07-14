"""The TwitterWatcher, using TweetStream."""

import logging
from julythontweets.watcher import Watcher
import re
from tornado.httpclient import AsyncHTTPClient
import tweetstream
import sys
import urlparse

# TODO: Extracting links from a tweet is wrong -- the watcher should
# call each add_callback() (not implemented yet) with the tweet and
# the callback should extract the link, parse the tweet, etc.

class MissingTwitterConfiguration(Exception):
    """Raised when a piece of configuration is missing for TwitterWatcher."""
    pass

class TwitterWatcher(Watcher):
    """
    Utilizes the TweetStream library to watch the Twitter stream
    for particular posts, etc.
    """

    def __init__(self, ioloop, callback, configuration):
        super(TwitterWatcher, self).__init__(ioloop, callback, configuration)
        self._configuration = configuration
        for key in [
                "twitter_consumer_key", "twitter_consumer_secret",
                "twitter_access_token", "twitter_access_token_secret",
                "twitter_search_term", "parsers", "callbacks"
            ]:
            value = configuration.get(key)
            if value is None:
                raise MissingTwitterConfiguration("Missing '%s'" % key)
            setattr(self, "_%s" % key, value)

    def start(self):
        """Attach to the IOLoop."""
        self._tweetstream = tweetstream.TweetStream(ioloop=self._ioloop,
            configuration=self._configuration)
        self._tweetstream.set_error_callback(self._error)
        self._tweetstream.fetch("/1/statuses/filter.json?track=%s" %
            self._twitter_search_term, callback=self.extract_from_tweet)

    def _error(self, error):
        logging.error("Error starting tweetstream: %s" % error)
        sys.exit(1)

    def extract_from_tweet(self, tweet):
        """Using the configured parsers, parse and post tweets."""
        # extract first link from a tweet
        if not tweet.get("text"):
            # not a valid tweet for parsing...
            return
        link_match = re.search(r"https?:\/\/[^\s]+", tweet["text"])

        def check_response(response):
            # we should have follwed all redirects to the end.
            self.parse(response.effective_url, tweet)

        def check_redirect(url):
            # tornado follows redirects by default
            client = AsyncHTTPClient(io_loop=self._ioloop)
            client.fetch(url, method="HEAD", callback=check_response)

        if link_match:
            # start the hunt for the 'final' URL
            check_redirect(link_match.group())
        else:
            logging.warning("Tweet contained no link: %s" % tweet["text"])
        cleaned = self._prepare_for_callbacks(tweet)
        for callback in self._callbacks:
            callback(cleaned)

    def _prepare_for_callbacks(self, tweet):
        """Normalizing minimal information for now."""
        cleaned_tweet = {}
        cleaned_tweet["username"] = tweet["user"]["screen_name"]
        cleaned_tweet["message"] = tweet["text"]
        cleaned_tweet["picture_url"] = tweet["user"]["profile_image_url"]
        return cleaned_tweet

    def parse(self, final_url, tweet):
        """Do what is necessary from the actual URL."""
        parsed = urlparse.urlparse(final_url)
        parser = self._parsers.get(parsed.netloc)
        if not parser:
            # fantastic. all this work and it's not configured.
            logging.warning("No configured parser for URL host %s" %
                parsed.host)
            return

        def format_for_callback(result):
            """
            Using the tweet and the result from github, finalize
            result and call the originally configured callback.
            (i.e. we actually have a valid tweet / commit.)

            """
            # we're assuming result is a dictionary -- dangerous?
            result["tweet"] = tweet
            self._callback(result)

        parser.parse(final_url, format_for_callback)
