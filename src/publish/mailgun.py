import logging

import requests
from requests.auth import HTTPBasicAuth

from utils.helper import articles_to_message
from utils.helper import settings
from utils.statics import TYPE_WARNING, MAILGUN_API_KEY, \
    MAILGUN_DOMAIN, EMAIL_RECIPIENTS, EMAIL_SENDER

log = logging.getLogger(__name__)


def mailgun_digest(articles, dry_run=False):
    send_mail(articles, 'Vulnerability Alert Digest', dry_run=dry_run)


def mailgun_warning(articles, dry_run=False):
    if not any([a['article_type'] == TYPE_WARNING for a in articles]):
        return

    warning_articles = list(filter(None,
                                   [article if article['article_type'] == TYPE_WARNING else None for article in
                                    articles]))
    send_mail(warning_articles, 'Vulnerability Alert Warning', dry_run=dry_run)


def send_mail(articles, subject, dry_run=False):
    msg = articles_to_message(articles, add_footer=True)

    if not msg:
        # Nothing to send
        return

    mailgun_api_key = settings[MAILGUN_API_KEY]
    mailgun_domain = settings[MAILGUN_DOMAIN]
    recipients = settings[EMAIL_RECIPIENTS]
    sender = settings[EMAIL_SENDER]

    for recipient in recipients:
        data = {
            'from': sender,
            'to': recipient,
            'subject': subject,
            'text': msg,
        }
        if dry_run:
            data['o:testmode'] = 'yes'
        r = requests.post(
            f'https://api.mailgun.net/v3/{mailgun_domain}/messages',
            auth=HTTPBasicAuth('api', mailgun_api_key),
            data=data)
        response_message = r.json().get('message')
        if r.status_code != 200 or 'Queued' not in response_message:
            log.warning(f'Sending mailgun email failed: {response_message}', extra=data)
