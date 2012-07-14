"""Loads configuration values from the ENVIRONMENT. """

import os

# Basic server configuration
PORT = int(os.environ.get("PORT") or 9000)
HOST = os.environ.get("HOST") or "localhost"

# Julython API configuration
JULYTHON_ENDPOINT_URL = os.environ.get("JULYTHON_ENDPOINT_URL") or \
    "http://localhost:8080/api/v1/commits"
JULYTHON_LIVE_ENDPOINT_URL = os.environ.get("JULYTHON_ENDPOINT_URL") or \
    "http://localhost:8080/api/v1/live"
JULYTHON_ENDPOINT_SECRET = os.environ.get("JULYTHON_ENDPOINT_SECRET") or \
    "foobar"

# Twitter configuration
TWITTER_CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY") or \
    "fakeconsumerkey"
TWITTER_CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET") or \
    "fakeconsumersecret"
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN") or \
    "fakeaccesstoken"
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET") \
    or "fakeaccesstokensecret"
TWITTER_SEARCH_TERM = os.environ.get("TWITTER_SEARCH_TERM") or "julython"


