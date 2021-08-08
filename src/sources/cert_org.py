from source_classes.rss import RSS
from utils.helper import truncate_string
from utils.statics import TYPE_VULNERABILITY, LANGUAGE_ENGLISH, TITLE_MAX_LENGTH


class CertOrg(RSS):
    name = 'cert.org'
    url = 'https://kb.cert.org/vuls/atomfeed/'
    main_type = TYPE_VULNERABILITY
    language = LANGUAGE_ENGLISH

    def process_articles(self):
        # Strip vulnerability note (e.g. "VU#357312") from title
        for article in self.articles:
            if article.title.startswith('VU#'):
                split_title = article.full_title.split(': ')
                article.full_title = ': '.join(split_title[1:])
                article.title = truncate_string(article.full_title, maxlen=TITLE_MAX_LENGTH)
