from article_database import ArticleDatabase
from collectors.collector_aws_news_blog import CollectorAWSNewsBlog
from collectors.collector_developersio import CollectorDevelopersIO
import logging

# ロガーの取得
logger = logging.getLogger(__name__)

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

def run_collectors():
    articles = []

    # AWS News Blogの記事を取得
    try:
        logger.info("AWS News Blogの記事を取得")
        collector_aws_news_blog = CollectorAWSNewsBlog()
        articles_aws_news_blog = collector_aws_news_blog.collect()
        articles.extend(articles_aws_news_blog)
    except Exception as e:
        logger.error(f"AWS News Blogの記事取得中にエラーが発生しました: {e}")

    # DevelopersIOの記事を取得
    try:
        logger.info("DevelopersIOの記事を取得")
        collector_developersio = CollectorDevelopersIO()
        articles_developersio = collector_developersio.collect()
        articles.extend(articles_developersio)
    except Exception as e:
        logger.error(f"DevelopersIOの記事取得中にエラーが発生しました: {e}")

    return articles

def get_articles(limit=20, page=0):
    with ArticleDatabase() as db:
        articles = db.select_all_articles(limit, page)
    return articles

def articles_to_markdown(articles):
    markdown = ""
    for article in articles:
        markdown += f"## [{article['title']}]({article['link']})\n"
        markdown += f"pub_date: {article['pub_date'].strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
        markdown += f"{article['description']}\n"
        markdown += f"キーワード: {article['categorys']}\n"
        markdown += f"ブログ: [{article['blog_name']}]({article['blog_url']}) より\n\n"
    return markdown

if __name__ == "__main__":
    logger.info("--------記事をDBに登録--------")
    articles = run_collectors()
    markdown = articles_to_markdown(articles)
    logger.info(markdown)
    logger.info("--------記事をDBから取得--------")
    articles = get_articles(limit=20, page=0)
    markdown = articles_to_markdown(articles)
    logger.info(markdown)
