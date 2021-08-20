import os
import sqlite3

from utils.helper import settings
from utils.statics import PUBLISH_TYPE_INSTANT, PUBLISH_TYPE_SUMMARY, DB_NAME, DB_PATH, DISCARD_ARTICLES_OLDER_THAN

db_path = settings.get(DB_PATH, '../')
db = os.path.join(db_path, DB_NAME)


def init_db():
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS articles
                     (url text primary key,
                     data_source text,
                     title text,
                     publish_time text,
                     article_type text,
                     instant_published integer,
                     summary_published integer,
                     UNIQUE(url));''')


def store_new_article(article, data_source, instant_published=False, summary_published=False):
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        statement = '''INSERT OR IGNORE INTO "articles" 
                     (title, data_source, publish_time, url, article_type, instant_published, summary_published) VALUES 
                     (?, ?, ?, ?, ?, ?, ?);'''
        c.execute(
            statement,
            (
                article.title,
                data_source,
                article.publish_time,
                article.url,
                article.article_type,
                instant_published,
                summary_published,
            )
        )


def fetch_unpublished(publish_type=PUBLISH_TYPE_INSTANT, regard_outdated=False):
    with sqlite3.connect(db) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        if regard_outdated:
            where_clause = ''
        else:
            discard_articles_older_than = settings.get(DISCARD_ARTICLES_OLDER_THAN, 3)
            where_clause = f'''AND publish_time > date('now', '-{discard_articles_older_than} days')'''
        if publish_type == PUBLISH_TYPE_INSTANT:
            statement = f'''SELECT * FROM articles where instant_published=false {where_clause} 
                            order by publish_time desc'''
        elif publish_type == PUBLISH_TYPE_SUMMARY:
            statement = f'''SELECT * FROM articles where summary_published=false {where_clause} 
                            order by publish_time desc'''
        else:
            raise NotImplemented(f'Publish type {publish_type} not implemented')
        result = [dict(r) for r in c.execute(statement)]
        return result


def mark_articles_published(urls, publish_type=PUBLISH_TYPE_INSTANT):
    with sqlite3.connect(db) as conn:
        c = conn.cursor()

        for url in urls:
            if publish_type == PUBLISH_TYPE_INSTANT:
                statement = '''UPDATE articles set instant_published=true where url=:url'''
            elif publish_type == PUBLISH_TYPE_SUMMARY:
                statement = '''UPDATE articles set summary_published=true where url=:url'''
            else:
                raise NotImplemented(f'Publish type {publish_type} not implemented')
            c.execute(statement, {'url': url})


def article_exists(title):
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        statement = 'SELECT title FROM articles where title=:title'
        c.execute(statement, {'title': title})
        if c.fetchone():
            return True
        else:
            return False
