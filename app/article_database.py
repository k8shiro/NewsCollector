import sqlite3
from datetime import datetime, timedelta, timezone
import os
import logging

# ロガーの取得
logger = logging.getLogger(__name__)

JST = timezone(timedelta(hours=+9), 'JST')


class ArticleDatabase:
    def __init__(self):
        db_file = os.environ.get('DB_PATH')
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        
        # テーブルが存在しない場合に作成
        # pub_dateはUNIXTIMEで保存
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                link TEXT UNIQUE,
                pub_date INTEGER,
                description TEXT,
                categorys TEXT,
                blog_name TEXT,
                blog_url TEXT,
                collect_date INTEGER
            )
        ''')
        self.conn.commit()

    def insert_article(self, article):
        try:
            self.cursor.execute('''
                INSERT INTO articles (title, link, pub_date, description, categorys, blog_name, blog_url, collect_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                article['title'],
                article['link'],
                int(article['pub_date'].timestamp()),
                article['description'],
                article['categorys'],
                article['blog_name'],
                article['blog_url'],
                int(article['collect_date'].timestamp())
            ))
            self.conn.commit()
            logger.info(f"記事を追加しました: {article['title']}")
            return True
        except sqlite3.IntegrityError:
            logger.info(f"記事はすでに存在します: {article['title']}")
            return False

    # 全権取得
    # limit: 取得する記事数
    # page: offsetするページ数
    def select_all_articles(self, limit, page=0):
        self.cursor.execute('''
            SELECT * FROM articles
            ORDER BY collect_date DESC
            LIMIT ? OFFSET ?
        ''', (limit, page * limit))
        articles = []
        for row in self.cursor.fetchall():
            article = {
                "title": row[1],
                "link": row[2],
                "pub_date": datetime.fromtimestamp(row[3], JST),
                "description": row[4],
                "categorys": row[5],
                "blog_name": row[6],
                "blog_url": row[7],
                "collect_date": datetime.fromtimestamp(row[8], JST)
            }
            articles.append(article)
        return articles

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    with ArticleDatabase() as db:
        articles = db.select_all_articles(limit=5)
        for article in articles:
            logger.info(article)