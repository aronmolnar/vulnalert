import uuid

import dateutil.parser
import yaml
from github import Github

from utils.helper import settings
from utils.statics import GITHUB_USER, GITHUB_PASSWORD, GITHUB_REPO


def jekyll_post(articles, dry_run=False):
    g = Github(settings[GITHUB_USER], settings[GITHUB_PASSWORD])
    repo = g.get_user().get_repo(settings[GITHUB_REPO])

    for article in articles:
        date = dateutil.parser.isoparse(article['publish_time']).strftime("%Y-%m-%d %H:%M %z")
        post_content = {
            'layout': 'post',
            'title': article['title'],
            'date': date,
            'category': article['article_type'].capitalize(),
            'source_url': article['url'],
        }
        post_content = f'---\n{yaml.dump(post_content)}---'
        filename = f'_posts/{date}-{uuid.uuid4()}.md'
        if dry_run:
            print("Jekyll dry run")
            print(post_content)
            continue
        repo.create_file(filename, 'Add article', post_content)
