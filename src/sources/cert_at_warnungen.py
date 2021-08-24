from source_classes.rss import RSS
from utils.statics import TYPE_WARNING, LANGUAGE_GERMAN


class CertAtWarnungen(RSS):
    name = 'cert.at Warnings'
    url = 'https://cert.at/cert-at.de.warnings.rss_2.0.xml'
    main_type = TYPE_WARNING
    language = LANGUAGE_GERMAN
