import xml.etree.ElementTree as ET
import urllib.request
from datetime import datetime
import json
from article_database import ArticleDatabase
import logging

# ロガーの取得
logger = logging.getLogger(__name__)


class CollectorDevelopersIO():
    def __init__(self):
        self.blog_name = "DevelopersIO: クラスメソッド発「やってみた」系技術メディア"
        self.blog_url = "https://dev.classmethod.jp/"
        self.rss_url = "https://dev.classmethod.jp/feed/"

    def collect(self):
        # RSSフィードを取得
        rss = urllib.request.urlopen(self.rss_url)
        tree = ET.parse(rss)
        root = tree.getroot()
        articles = []

        # RSSフィードから記事情報を取得し、DBに追加
        with ArticleDatabase() as db:
            for item in root.findall(".//item"):
                title = item.find("title").text
                link = item.find("link").text
                pub_date = item.find("pubDate").text
                pub_date = pub_date.replace("GMT", "+0000")
                pub_date = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")
                description = item.find("description").text
                categorys = item.findall("category")
                categorys = [category.text for category in categorys]
                categorys = ', '.join(categorys)

                article = {
                    "title": title,
                    "link": link,
                    "pub_date": pub_date,
                    "description": description,
                    "categorys": categorys,
                    "blog_name": self.blog_name,
                    "blog_url": self.blog_url,
                    "collect_date": datetime.now()
                }

                # データベースに記事を追加
                success_insert = db.insert_article(article)
                if success_insert:
                    articles.append(article)
        return articles

if __name__ == "__main__":
    collector = CollectorDevelopersIO()
    collector.collect()
