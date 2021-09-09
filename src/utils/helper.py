import html
import os
import random
from json import JSONDecodeError

import requests
import yaml

from utils.statics import TYPE_WARNING, TYPE_EXPLOIT, TYPE_FEATURED, TYPE_VULNERABILITY, EMAIL_FOOTER, SETTINGS_PATH, \
    SETTINGS_FILENAME, SETTINGS_FILENAME_ENV, RANDOM_PS

settings_filname = os.environ.get(SETTINGS_FILENAME_ENV, SETTINGS_FILENAME)
SETTINGS_FILE = os.path.join(os.environ.get(SETTINGS_PATH, '../'), settings_filname)
HEADLINES = {
    TYPE_VULNERABILITY: 'Vulnerabilities',
    TYPE_WARNING: 'Warnings',
    TYPE_EXPLOIT: 'Exploits',
    TYPE_FEATURED: 'Featured',
}
MIN_RANDOM_INFO_SAMPLE = 20


def get_settings():
    try:
        with open(SETTINGS_FILE, 'r') as f:
            settings = yaml.safe_load(f)
        return settings
    except FileNotFoundError:
        return dict()


settings = get_settings()


def translate(text, src='de', dest='en'):
    r = requests.get('https://clients5.google.com/translate_a/t',
                     params={'client': 'dict-chrome-ex',
                             'sl': src,
                             'tl': dest,
                             'q': text})
    if r.status_code == 200:
        try:
            sentences = r.json().get('sentences')
            return ' '.join(s['trans'].strip() for s in sentences)
        except (IndexError, ValueError, JSONDecodeError):
            pass
    return None


def articles_to_message(
        articles,
        add_footer=False,
        unsubscribe_link=None,
        unescape_html=False,
        include_random_info=False):
    msg = list()

    for article_type in [TYPE_WARNING, TYPE_VULNERABILITY, TYPE_EXPLOIT, TYPE_FEATURED]:
        if any([a['article_type'] == article_type for a in articles]):
            msg.append(f"# {HEADLINES[article_type]}")
        else:
            # This article type is not present and therefore needs not headline
            continue

        for article in articles:
            if article['article_type'] == article_type:
                title = html.unescape(article["title"]) if unescape_html else article["title"]
                msg.append(
                    f'* {title}: {article["url"]}')

        msg.append('')  # newline between article types

    if not msg:
        # No need to add footer or anything else
        return None

    if include_random_info:
        i = random.randint(0, max(MIN_RANDOM_INFO_SAMPLE, len(settings[RANDOM_PS]) - 1))
        random_info = None
        try:
            random_info = settings[RANDOM_PS][i]
        except (TypeError, IndexError):
            pass
        if random_info:
            msg.extend([f'PS: {random_info}', ''])

    if add_footer:
        if EMAIL_FOOTER in settings:
            msg.append(f'\n{settings[EMAIL_FOOTER]}')
        if unsubscribe_link:
            msg.append(f'\nUnsubscribe at {unsubscribe_link}')

    msg = '\n'.join(msg)
    return msg


def truncate_string(string, maxlen):
    if len(string) <= maxlen:
        return string
    if maxlen <= 3:
        raise ValueError('maxlen must be greater than 3.')

    string = string[:maxlen - 2]
    index = string.rfind(' ')
    if index == -1:
        # Did not find a space
        string = string[:-1]
    else:
        string = string[:index]
    return f'{string}...'
