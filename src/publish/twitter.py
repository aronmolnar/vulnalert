import html

import tweepy

from utils.helper import settings, truncate_string
from utils.statics import TWITTER_API_KEY, TWITTER_API_SECRET_KEY, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET

TWEET_LENGTH = 280
URL_LENGTH = 23  # URLs in tweets will always be altered to 23 characters
PUNCTUATION_CHARS = 10
TITLE_MAX_LENGTH = TWEET_LENGTH - URL_LENGTH - PUNCTUATION_CHARS


def tweet(articles, dry_run=False):
    if not dry_run:
        auth = tweepy.OAuthHandler(settings[TWITTER_API_KEY], settings[TWITTER_API_SECRET_KEY])
        auth.set_access_token(settings[TWITTER_ACCESS_TOKEN], settings[TWITTER_ACCESS_TOKEN_SECRET])
        api = tweepy.API(auth)

    for article in articles:
        title = html.unescape(article["title"])
        title = truncate_string(title, maxlen=TITLE_MAX_LENGTH)
        msg = f'{title} {article["url"]}'
        if dry_run:
            print('Twitter', msg)
            continue
        api.update_status(status=msg)
