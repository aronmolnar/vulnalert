import datetime
import logging

import click

from sources.cert_at_warnungen import CertAtWarnungen
from sources.cert_org import CertOrg
from sources.cyber_gov_au import CyberGovAu
from sources.exploit_db import ExploitDatabase
from sources.heise_alerts import HeiseAlerts
from sources.nuclei import Nuclei
from utils.db import init_db, fetch_unpublished, mark_articles_published
from utils.helper import settings
from utils.mappings import PUBLISH_TYPES
from utils.statics import PUBLISH_TYPE_SUMMARY, PUBLISH_TYPE_INSTANT, OMIT_WEEKDAYS

log = logging.getLogger(__name__)
sources = [CyberGovAu, CertAtWarnungen, HeiseAlerts, ExploitDatabase, CertOrg, Nuclei]


@click.command()
@click.option('--publish-instant/--no-publish-instant', default=False)
@click.option('--publish-summary/--no-publish-summary', default=True)
@click.option('--dry-run/--no-dry-run', default=True)
def run(publish_instant, publish_summary, dry_run):
    if dry_run:
        log.warning('Dry run. Nothing will be published.')
    init_db()

    # Fetch sources
    for source in sources:
        source()

    # Publish
    publish = []
    if publish_instant:
        publish.append(PUBLISH_TYPE_INSTANT)
    if publish_summary:
        if datetime.datetime.today().strftime('%A') not in settings.get(OMIT_WEEKDAYS, list()):
            publish.append(PUBLISH_TYPE_SUMMARY)

    for publish_type in publish:
        instant_publish_methods = settings.get(publish_type, list())
        articles = fetch_unpublished(publish_type=publish_type)
        for publish_method in instant_publish_methods:
            publish_method = PUBLISH_TYPES[publish_method]
            publish_method(articles, dry_run=dry_run)

        # Mark as instant published
        if not dry_run:
            urls = [article['url'] for article in articles]
            mark_articles_published(urls, publish_type=publish_type)


if __name__ == "__main__":
    run()
