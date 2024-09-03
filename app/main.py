from articles import run_collectors
from teams import send_to_teams
from logging_config import setup_logging
import logging

# ログ設定を読み込む
setup_logging()
# ロガーの取得
logger = logging.getLogger(__name__)



def main():
    logger.info("--------開始--------")
    articles = run_collectors()
    send_to_teams(articles)
    logger.info("--------終了--------")


if __name__ == "__main__":
    main()