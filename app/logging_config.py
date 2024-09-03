import logging


def setup_logging():
    # ルートロガーの設定
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # ログレベルをDEBUGに設定

    # コンソールハンドラーを設定
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # コンソール出力のログレベル
    console_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    console_handler.setFormatter(console_formatter)

    # ファイルハンドラーを設定
    file_handler = logging.FileHandler('/log/app.log')
    file_handler.setLevel(logging.INFO)  # ファイル出力のログレベル
    file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    file_handler.setFormatter(file_formatter)

    # ハンドラーをルートロガーに追加
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

