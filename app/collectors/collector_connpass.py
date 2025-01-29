import xml.etree.ElementTree as ET
import urllib.request
from datetime import datetime
import json
from article_database import ArticleDatabase
import logging

# ロガーの取得
logger = logging.getLogger(__name__)


class CollectorConnpass():
    def __init__(self):
        self.blog_name = "Connpass: エンジニアをつなぐIT勉強会支援プラットフォーム"
        self.blog_url = "https://connpass.com/"
        self.rss_url = "https://connpass.com/explore/ja.atom"

    def collect(self):
        # RSSフィードを取得
        rss = urllib.request.urlopen(self.rss_url)
        rss = rss.read().decode('utf-8')
        root = ET.fromstring(rss)
        articles = []

        # Atomの名前空間を考慮
        ns = {'atom': 'http://www.w3.org/2005/Atom'}

        # RSSフィードから記事情報を取得し、DBに追加
        with ArticleDatabase() as db:
            for item in root.findall("atom:entry", ns):
                title = item.find("atom:title", ns).text
                link = item.find("atom:link", ns).attrib.get("href")
                pub_date = item.find("atom:published", ns).text
                pub_date = pub_date.replace("+09:00", " +0900")
                pub_date = datetime.strptime(pub_date, "%Y-%m-%dT%H:%M:%S %z")
                description = item.find("atom:summary", ns).text
                categorys = ''

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

        # Connpassの新着イベントは一つのPostにまとめる
        description = "新着イベント \n" + "\n".join([f"- [{article['title']}]({article['link']})" for article in articles])
        new_events = [{
            "title": f"Connpass新着イベント {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}",
            "link": "https://connpass.com/explore/",
            "pub_date": datetime.now(),
            "description": description,
            "categorys": "",
            "blog_name": self.blog_name,
            "blog_url": self.blog_url,
            "collect_date": datetime.now()
        }]

        print(new_events)

        return new_events


if __name__ == "__main__":
    collector = CollectorConnpass()
    collector.collect()
