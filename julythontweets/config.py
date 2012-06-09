"""Loads configuration values from the ENVIRONMENT. """

import os

# Basic server configuration
PORT = int(os.environ.get("PORT") or 9000)
HOST = os.environ.get("HOST") or "localhost"

# Julython API configuration
JULYTHON_ENDPOINT_URL = os.environ.get("JULYTHON_ENDPOINT_URL") or \
    "http://localhost:8080/api/v1/commits"
JULYTHON_ENDPOINT_SECRET = os.environ.get("JULYTHON_ENDPOINT_SECRET") or \
    "foobar"

# Twitter configuration
TWITTER_USERNAME = os.environ.get("TWITTER_USERNAME") or "faketwitter"
TWITTER_PASSWORD = os.environ.get("TWITTER_PASSWORD") or "fakepassword"



