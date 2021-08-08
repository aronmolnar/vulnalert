import logging
from datetime import datetime, timedelta

from utils.db import store_new_article
from utils.helper import settings
from utils.helper import truncate_string
from utils.statics import TYPE_UNKNOWN, LANGUAGE_UNKNOWN, TITLE_MAX_LENGTH, DISCARD_ARTICLES_OLDER_THAN

log = logging.getLogger(__name__)


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
            if article.article_type != TYPE_UNKNOWN:
                store_new_article(article, data_source=self.name)
            else:
                log.warning(f'Article {self.url} is of unknown type and will not be processed')

    def fetch(self):
        pass

    def process_articles(self):
        pass


class Article:
    def __init__(self, title, url, publish_time, article_type):
        self.full_title = title
        self.title = truncate_string(title, maxlen=TITLE_MAX_LENGTH)
        self.url = url
        self.publish_time = publish_time
        self.article_type = article_type

        discard_articles_older_than = settings.get(DISCARD_ARTICLES_OLDER_THAN, 3)
        discard_articles_older_than = timedelta(days=discard_articles_older_than)

        if self.publish_time and (datetime.now() - self.publish_time) > discard_articles_older_than:
            self.outdated = True
        else:
            self.outdated = False
