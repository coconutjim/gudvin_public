from requests_oauthlib import OAuth1

from log import log

TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_KEY_SECRET = ''
TWITTER_ACCESS_TOKEN = ''
TWITTER_ACCESS_TOKEN_SECRET = ''
TWITTER_OAUTH = None


def setup_twitter_connection():
    global TWITTER_OAUTH
    log('setting up twitter connection...')
    TWITTER_OAUTH = OAuth1(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_KEY_SECRET,
                           TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    log('set up twitter connection...')

