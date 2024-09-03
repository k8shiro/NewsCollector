# 情報収集用ツール

# 使い方

docker compose up -d で起動する。  
起動すると compose の app サービスが起動し、その中で main.py が実行される。  
main.py による記事の収集と Teams への投稿を行った後、コンテナは終了する。

定期実行は、開発インスタンスの`~/.bashrc`に docker compose up -d を記述しておくことで、定期実行の代わりとする。
