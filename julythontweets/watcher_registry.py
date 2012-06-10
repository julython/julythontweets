"""Helper functions for registering and configuring IOLoop watchers."""

from julythontweets import config
from julythontweets.parsers.github_parser import GitHubParser
from julythontweets.watchers.twitter_watcher import TwitterWatcher


def dummy_callback(commit):
    """Placeholder until we hit the API."""
    print commit


def register_watchers(ioloop):
    """
    Registers watchers to the ioloop. Eventually, this will be
    configurable somewhere...
    """
    twitter_config = get_watcher_configuration("twitter", ioloop)
    twitter_watcher = TwitterWatcher(ioloop, dummy_callback, twitter_config)
    twitter_watcher.start()

def get_watcher_configuration(watcher_name, ioloop):
    """Retrieves configuration based on watcher name."""
    configuration = {
        "twitter": _get_twitter_configuration(ioloop),
    }.get(watcher_name)
    return configuration

def _get_twitter_configuration(ioloop):
    """Build twitter configuration."""
    # parser stuff should be moved into parser_registry module.
    github_parser = GitHubParser(ioloop, {})
    return {
        "twitter_consumer_key": config.TWITTER_CONSUMER_KEY,
        "twitter_consumer_secret": config.TWITTER_CONSUMER_SECRET,
        "twitter_access_token": config.TWITTER_ACCESS_TOKEN,
        "twitter_access_token_secret": config.TWITTER_ACCESS_TOKEN_SECRET,
        "twitter_search_term": config.TWITTER_SEARCH_TERM,
        "parsers": {
            "github.com": github_parser,
            "www.github.com": github_parser
        }
    }


