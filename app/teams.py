import urllib.request
import json
import os
import logging
import time

# ロガーの取得
logger = logging.getLogger(__name__)


WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
# articleは以下のような形式の辞書型
# {
#     "title": "string",
#     "link": "string",
#     "pub_date": datetime.datetime,
#     "description": "string",
#     "categorys": "string",
#     "blog_name": "string",
#     "blog_url": "string",
#     "collect_date": datetime.datetime
# }

def send_to_teams(articles):
    if len(articles) == 0:
        logger.info("新着記事がありません")
        return

    body_items = []
    line_num = 0
    for article in articles:
        body_item = [{
            "type": "TextBlock",
            "text": article['title'],
            "weight": "Bolder",
            "size": "Large",
            "wrap": True,
            "spacing": "None"
        }, {
            "type": "TextBlock",
            "text": article['pub_date'].strftime('%Y-%m-%d %H:%M:%S %Z'),
            "isSubtle": True,
            "wrap": True,
            "spacing": "None"
        }, {
            "type": "TextBlock",
            "text": article['description'],
            "wrap": True,
            "spacing": "Medium"
        }, {
            "type": "TextBlock",
            "text": article['categorys'],
            "weight": "Bolder",
            "isSubtle": True,
            "spacing": "Small"
        }, {
            "type": "TextBlock",
            "text": f"[記事を読む]({article['link']})",
            "wrap": True,
            "spacing": "Small"
        }, {
            "type": "TextBlock",
            "text": f"ブログ: [{article['blog_name']}]({article['blog_url']}) より",
            "wrap": True,
            "isSubtle": True,
            "spacing": "Small"
        }, {
            "type": "TextBlock",
            "text": f"Collected on: {article['collect_date'].strftime('%Y-%m-%d %H:%M:%S %Z')}",
            "isSubtle": True,
            "wrap": True,
            "spacing": "Medium"
        }, {
            "type": "TextBlock",
            "text": "--------------------------------------",
            "weight": "Lighter",
            "wrap": True,
            "spacing": "Medium",
            "separator": True
        }]
        line_num = len(body_item)
        body_items.extend(body_item)
        

    chunk_size = line_num * 6 # 1itemにつきline_num行 * 6アイテム
    post_groups = [body_items[i:i + chunk_size] for i in range(0, len(body_items), chunk_size)]

    for items in post_groups:
        message = {
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": {
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "version": "1.2",
                        "body": items,
                        "msteams": {
                            "width": "Full"
                        }
                    }
                }
            ]
        }
        headers = {
            'Content-Type': 'application/json'
        }
        req = urllib.request.Request(WEBHOOK_URL, json.dumps(message).encode(), headers)
        with urllib.request.urlopen(req) as res:
            body = res.read()
            logger.info(body)
        time.sleep(10)

if __name__ == "__main__":
    from datetime import datetime
    articles = [
        {
            "title": "AWSの新機能が発表されました(テスト用投稿1)",
            "link": "https://aws.amazon.com/jp/new-feature",
            "pub_date": datetime.now(),
            "description": "AWSで＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊の新機能が発表されました。詳細は＊＊＊＊＊＊で＊＊＊＊＊＊＊＊＊＊＊＊＊＊で＊＊＊＊＊＊＊＊＊＊＊です。使用料金は＊＊＊＊＊＊＊＊＊＊＊",
            "categorys": "新機能, AWS",
            "blog_name": "Amazon Web Services ブログ",
            "blog_url": "https://aws.amazon.com/jp/blogs/news/",
            "collect_date": datetime.now()
        }, {
            "title": "AWSの新機能が発表されました(テスト用投稿2)",
            "link": "https://aws.amazon.com/jp/new-feature",
            "pub_date": datetime.now(),
            "description": "新機能が発表されました。＊＊＊＊＊と比較して＊＊＊＊＊＊＊＊＊＊＊＊＊＊であり＊＊＊＊＊＊＊＊＊＊＊＊＊＊です。",
            "categorys": "新機能, AWS",
            "blog_name": "Amazon Web Services ブログ",
            "blog_url": "https://aws.amazon.com/jp/blogs/news/",
            "collect_date": datetime.now()
        }
    ]
    send_to_teams(articles)

