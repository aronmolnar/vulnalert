import socket
from datetime import datetime

import feedparser

from source_classes.base import Source, Article


class RSS(Source):
    pass

    def fetch(self):
        socket.setdefaulttimeout(5)
        parsed_feed = feedparser.parse(self.url)
        for entry in parsed_feed.get('entries', list()):
            article = Article(
                title=entry['title'],
                url=entry['id'],
                publish_time=datetime(*entry['published_parsed'][:6]),
                article_type=self.main_type,
            )
            if article.outdated or not article.new:
                break
            self.articles.append(article)
