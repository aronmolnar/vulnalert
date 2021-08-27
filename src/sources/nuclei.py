import os
import tempfile

import git
import yaml
from dateutil.parser import parse

from source_classes.base import Source, Article
from utils.statics import TYPE_EXPLOIT, LANGUAGE_ENGLISH


class Nuclei(Source):
    name = 'nuclei'
    url = 'https://github.com/projectdiscovery/nuclei-templates.git'
    url_prefix = 'https://github.com/projectdiscovery/nuclei-templates/blob/master/'
    main_type = TYPE_EXPLOIT
    language = LANGUAGE_ENGLISH

    exclude_by_reference = ['www.exploit-db.com/exploits']
    fetch_since = '48 hours ago'
    include_severity = ['high', 'critical']

    def fetch(self):
        nuclei_path = os.path.join(tempfile.gettempdir(), 'nuclei-templates')
        try:
            os.makedirs(nuclei_path)
        except FileExistsError:
            pass

        try:
            git.Repo.clone_from(self.url, nuclei_path)
        except git.GitCommandError:
            # Repo probably exists, so pull it
            repo = git.cmd.Git(nuclei_path)
            repo.pull()

        g = git.Git(nuclei_path)
        commits = dict.fromkeys(
            [c.strip('"') for c in g.log(f'--since={self.fetch_since}', '--pretty=format:"%H"').split('\n')])

        for commit in commits:
            commits[commit] = g.diff_tree(
                '-r',
                '--find-copies-harder',
                '--find-renames',
                '--diff-filter', 'A',
                '--name-only',
                '--no-commit-id', commit
            ).split()

        for commit, added_files in commits.items():
            for filename in added_files:
                try:
                    with open(os.path.join(nuclei_path, filename), 'r') as f:
                        contents = yaml.safe_load(f)
                except FileNotFoundError:
                    # File was probably renamed
                    # This might cause that we miss some new files TODO
                    continue

                severity = contents.get('info', dict()).get('severity') or ''
                if severity.lower() not in self.include_severity:
                    continue
                references = contents.get('info', dict()).get('reference') or list()
                if any([True for r in self.exclude_by_reference for ref in references if r in ref]):
                    continue

                title = contents.get('info', dict()).get('name')
                url = f'{self.url_prefix}{filename}'
                date = g.show('-s', '--format=%ci', commit)
                try:
                    date = parse(date).replace(tzinfo=None)
                except ValueError:
                    # Don't know the date
                    continue

                article = Article(
                    title=title,
                    url=url,
                    publish_time=date,
                    article_type=self.main_type,
                    language=self.language,
                )
                if article.outdated:
                    break
                self.articles.append(article)
