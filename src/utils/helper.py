import os

import yaml

from utils.statics import TYPE_WARNING, TYPE_EXPLOIT, TYPE_FEATURED, TYPE_VULNERABILITY, EMAIL_FOOTER, SETTINGS_PATH, \
    SETTINGS_FILENAME, SETTINGS_FILENAME_ENV

settings_filname = os.environ.get(SETTINGS_FILENAME_ENV, SETTINGS_FILENAME)
SETTINGS_FILE = os.path.join(os.environ.get(SETTINGS_PATH, '../'), settings_filname)


def get_settings():
    try:
        with open(SETTINGS_FILE, 'r') as f:
            settings = yaml.safe_load(f)
        return settings
    except FileNotFoundError:
        return dict()


settings = get_settings()


def articles_to_message(articles, add_footer=False, unsubscribe_link=None):
    msg = list()

    for article_type in [TYPE_WARNING, TYPE_VULNERABILITY, TYPE_EXPLOIT, TYPE_FEATURED]:
        if any([a['article_type'] == article_type for a in articles]):
            msg.append(f"# {article_type.capitalize()}")
        else:
            # This article type is not present and therefore needs not headline
            continue

        for article in articles:
            if article['article_type'] == article_type:
                msg.append(f'"{article["title"]}": {article["url"]}')

        msg.append('')  # newline between article types

    if not msg:
        # No need to add footer or anything else
        return None

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
