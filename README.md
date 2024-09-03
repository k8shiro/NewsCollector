# 情報収集用ツール

# 使い方

## 定期実行

docker compose up -d で起動する。  
起動すると compose の app サービスが起動し、その中で main.py が実行される。  
main.py による記事の収集と Teams への投稿を行った後、コンテナは終了する。

定期実行は、

```
/etc/systemd/system/newscollector.service
```

に設定されているサービスを

```
sudo systemctl enable newscollector.service
```

で起動時に実行されるようにしている。

## DB の確認

sqlite の viewer を入れている。
localhost:8765 でアクセスできる。
