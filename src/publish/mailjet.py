import logging

import requests
from requests.auth import HTTPBasicAuth

from utils.helper import articles_to_message
from utils.helper import settings
from utils.statics import TYPE_WARNING, MAILJET_API_KEY, MAILJET_SECRET_KEY, SENT_TO_MAILJET_CONTACT_LIST, \
    EMAIL_RECIPIENTS, EMAIL_SENDER, EMAIL_SENDER_NAME, MAILJET_CONTACT_LIST_ID

log = logging.getLogger(__name__)


def mailjet_digest(articles, dry_run=False):
    send_mail(articles, 'Vulnerability Alert Digest', dry_run=dry_run)


def mailjet_warning(articles, dry_run=False):
    if not any([a['article_type'] == TYPE_WARNING for a in articles]):
        return

    warning_articles = list(filter(None,
                                   [article if article['article_type'] == TYPE_WARNING else None for article in
                                    articles]))
    send_mail(warning_articles, 'Vulnerability Alert Warning', dry_run=dry_run)


def send_mail(articles, subject, dry_run=False):
    msg = articles_to_message(articles, add_footer=True, unsubscribe_link='[[UNSUB_LINK]]', unescape_html=True)
    if not msg:
        # Nothing to send
        return

    if settings.get(SENT_TO_MAILJET_CONTACT_LIST):
        recipients = get_mailjet_contacts()
    else:
        recipients = settings[EMAIL_RECIPIENTS]

    if not recipients:
        return

    mailjet_api_key = settings[MAILJET_API_KEY]
    mailjet_secret_key = settings[MAILJET_SECRET_KEY]
    sender_mail = settings[EMAIL_SENDER]
    sender_name = settings[EMAIL_SENDER_NAME]

    data = {
        'Globals': {
            'From': {
                'Email': sender_mail,
                'Name': sender_name,
            },
            'Subject': subject,
            'TextPart': msg,
        },
        'Messages': []
    }
    for recipient in recipients:
        data['Messages'].append({"To": [{"Email": recipient, }], })

    if not dry_run:
        r = requests.post(
            'https://api.mailjet.com/v3.1/send',
            auth=HTTPBasicAuth(mailjet_api_key, mailjet_secret_key),
            json=data)

        if r.status_code != 200:
            log.warning(f'Sending mailjet email failed: {r.text}', extra=data)


def get_mailjet_contacts():
    mailjet_api_key = settings[MAILJET_API_KEY]
    mailjet_secret_key = settings[MAILJET_SECRET_KEY]
    mailjet_contact_list_id = settings[MAILJET_CONTACT_LIST_ID]

    r = requests.get(
        f'https://api.mailjet.com/v3/REST/contactslist/{mailjet_contact_list_id}',
        auth=HTTPBasicAuth(mailjet_api_key, mailjet_secret_key),
    )
    if r.status_code != 200:
        log.warning(f"Retrieving Mailjet contact list failed: {r.text}")
        return list()

    r_json = r.json()
    if r_json.get('Count') == 1:
        return [f'{r_json["Data"][0]["Address"]}@lists.mailjet.com']
