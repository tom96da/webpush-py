# webpush-py

[English](README.md) | 日本語

## プロジェクト概要

このプロジェクトは、PythonとFastAPIを使用してプッシュ通知を実装する方法を示しています。ユーザーは、いくつかの簡単な手順に従うことで、プッシュ通知を簡単に体験できます。このプロジェクトには、ユーザーがプッシュ通知を購読し、リアルタイムで受信できるWebインターフェースが含まれています。

## 特徴

- 簡単なセットアップと構成
- Dockerを使用したコンテナ化
- 安全な通信のための自己署名SSL証明書の生成
- プッシュ通知を処理するサービスワーカーの登録
- ユーザーがプッシュ通知を購読および購読解除できる
- 簡単なスクリプトを使用してプッシュ通知を送信

## プッシュ通知を体験する方法

1. リポジトリをクローンする:
    ```bash
    git clone https://github.com/tom96da/webpush-py.git
    cd webpush-py
    ```

2. nginx用のサーバー証明書を生成し、Dockerコンテナをビルドする:
    ```bash
    source build.sh
    ```

3. サーバー証明書をブラウザにインポートしてSSLの警告を回避する。証明書は `nginx/ssl/server.crt` にあります。

4. ブラウザからトップページにアクセスしてプッシュ通知を有効にする:
    - ブラウザを開き、`https://localhost` にアクセスします。
    - "Push Notifications" チェックボックスをチェックして購読します。
    - 注意: ページにアクセスするとサービスワーカーが登録されます。サーバーの自己署名証明書がブラウザに認められていることを確認してください。

5. 通知を発行し、ブラウザが受信することを確認する:
    ```bash
    source publish.sh
    ```

## API エンドポイント

| メソッド | エンドポイント            | 説明                                      |
|----------|---------------------------|-------------------------------------------|
| GET      | /health                   | サーバーのヘルスステータスを確認する      |
| GET      | /                         | ホームページにアクセスする                |
| GET      | /vapid-public-key         | VAPID公開鍵を取得する                     |
| POST     | /publish                  | プッシュ通知を発行する                    |
| POST     | /subscribe                | プッシュ通知を購読する                    |
| POST     | /unsubscribe              | プッシュ通知の購読を解除する              |
