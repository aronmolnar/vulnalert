import html
import logging
from datetime import datetime, timedelta

from googletrans import Translator

from utils.db import store_new_article, article_exists
from utils.helper import settings
from utils.helper import truncate_string
from utils.statics import TYPE_UNKNOWN, LANGUAGE_UNKNOWN, LANGUAGE_ENGLISH, TITLE_MAX_LENGTH, \
    DISCARD_ARTICLES_OLDER_THAN

log = logging.getLogger(__name__)
LOCAL_CLIENTS = ['chrome', 'firefox', 'edge', 'opera', 'thunderbird']


class Source:
    name = None
    url = None
    disabled = False
    articles = None
    main_type = TYPE_UNKNOWN
    language = LANGUAGE_UNKNOWN

    def __init__(self):
        if self.disabled:
            return
        self.articles = list()
        self.fetch()
        self.process_articles()
        for article in self.articles:
            if article.article_type == TYPE_UNKNOWN:
                log.warning(f'Article {self.url} is of unknown type and will not be processed')
                continue

            if any(c.lower() in article.full_title.lower() for c in LOCAL_CLIENTS):
                # Ignore vulnerabilities of local clients
                continue

            if article.new:
                store_new_article(article, data_source=self.name)

    def fetch(self):
        pass

    def process_articles(self):
        pass


class Article:
    def __init__(self, title, url, publish_time, article_type, language):
        translator = Translator()
        self.language = language

        self.full_title = html.escape(title)
        if self.language != LANGUAGE_ENGLISH:
            self.full_title = translator.translate(title, dest='en').text
        self.title = truncate_string(self.full_title, maxlen=TITLE_MAX_LENGTH)
        self.url = url
        self.publish_time = publish_time
        self.article_type = article_type

        discard_articles_older_than = settings.get(DISCARD_ARTICLES_OLDER_THAN, 3)
        discard_articles_older_than = timedelta(days=discard_articles_older_than)

        if self.publish_time and (datetime.now() - self.publish_time) > discard_articles_older_than:
            self.outdated = True
        else:
            self.outdated = False

        if article_exists(self.title):
            self.new = False
        else:
            self.new = True
