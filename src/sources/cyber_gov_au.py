import logging

import dateutil.parser
import requests
from bs4 import BeautifulSoup

from source_classes.base import Source, Article
from utils.statics import TYPE_VULNERABILITY, TYPE_WARNING, LANGUAGE_ENGLISH

log = logging.getLogger(__name__)


class CyberGovAu(Source):
    name = 'cyber.gov.au'
    origin = 'https://www.cyber.gov.au'
    url = f'{origin}/acsc/view-all-content/alerts'
    main_type = TYPE_VULNERABILITY
    language = LANGUAGE_ENGLISH
    alert_status_type_mapping = {
        'HIGH': TYPE_VULNERABILITY,
        'CRITICAL': TYPE_WARNING,
    }

    def fetch(self, ):
        r = requests.get(self.url)
        if r.status_code != 200:
            log.warning('Did not reach URL.')
            return
        soup = BeautifulSoup(r.text, features="html.parser")
        articles_html = soup.find_all("div", {"class": "views-row"})
        for article in articles_html:
            try:
                date = article.find("p", attrs={"class": "acsc-date"})
                alert_status = date.find("span").text
                if alert_status not in self.alert_status_type_mapping:
                    continue
                title = article.find("p", attrs={"class": "acsc-title"}).text
                url = article.find("a", href=True)
                date = date.text.split('-')[0].strip()
            except AttributeError:
                continue
            try:
                date = dateutil.parser.parse(date)
                url = f'{self.origin}{url["href"]}'
            except (ValueError, TypeError):
                log.warning('Processing data failed. Did HTML structure change?')

            self.articles.append(
                Article(
                    title=title,
                    url=url,
                    publish_time=date,
                    article_type=self.alert_status_type_mapping[alert_status],
                    language=self.language,
                ))
