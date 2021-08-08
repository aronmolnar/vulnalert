from source_classes.rss import RSS
from utils.statics import TYPE_VULNERABILITY, LANGUAGE_GERMAN


class HeiseAlerts(RSS):
    name = 'Heise Alerts'
    url = 'https://www.heise.de/security/rss/alert-news.rdf'
    main_type = TYPE_VULNERABILITY
    language = LANGUAGE_GERMAN
