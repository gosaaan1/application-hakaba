# サポアス

## 機能

## 共通

### コンテナのビルド

```
cd spus16_bot/
docker build . -t spus16_bot:latest
```

### 環境変数

環境変数には以下の値を含める必要があります。

```
# DATABASE
database_uri=sqlite:///spus16_bot.sqlite3
# TWITTER
consumer_key={Twitterのconsumer_key}
consumer_secret={Twitterのcunsumer_secret}
access_token_key={Twitterのaccess_token_key}
access_token_secret={Twitterのaccess_token_secret}
# Azure
subscription_key={Microsoft Azureのサブスクリプションキー}
# Behavior Options
log_level={DEBUG|INFO|WARN|ERROR}       ... 省略時は INFO で動作します
test_mode={空白以外ならテストモード有効}    ... 実際にツイートを行ないません
```

## 呟怖お題画像著作権チェック

「#このお題で呟怖をください」のハッシュタグを含む画像付きツイートを検索し、Bing画像検索でヒットするWebサイトがないか調べる。無ければ「いいね」する。あればTwitterのリストに追加する。

### 環境変数

共通の環境変数に下記の環境変数を追加します。

* spus16_traffic.env

    ```
    list_id={チェックに引っかかったユーザーの追加先TwitterのリストID}
    query={ツイートを検索するためのクエリ}
    match_words={チェック対象にするツイートに含むキーワード
    ```

### 実行

```
docker run -it --name=spus_tbkw --env-file=spus16_tbkw.env spus16_bot:latest python /usr/src/app/bot_favorite.py
```

### 課題

* `Ver.0.1.1`で試験運転中。

## 運行情報

Twitterのリストに登録された鉄道会社公式アカウントのツイートをもとに、遅延情報をリツイートする。
「路線名」のハッシュタグと「公式アカウント名（複数ある場合）」を付与してリツイートする。

### 環境変数

共通の環境変数に下記の環境変数を追加します。

* spus16_traffic.env

    ```
    list_id={TwitterのリストID}
    state_words={ツイートを抽出する単語を正規表現で指定}
    place_words={ハッシュタグにする単語を正規表現で指定}
    ```

※単語の解析に`janome`を使用しています。正しく認識できない単語は `service/user_dic.csv` に追加することができます。

### 実行

```
docker run -it --name=spus_traffic --env-file=spus16_traffic.env spus16_bot:latest python /usr/src/app/bot_traffic.py
```

### 課題

* `Ver.0.2.0`で試験運転中。

## 避難啓蒙

Twitterリストに登録されたニュースアカウントのツイートをもとに、避難指示情報をリツイートする。
「都道府県名」「市区町村」のハッシュタグをツイート中から抽出・付与してリツイートする。
避難先や避難方法に関する発信を行うことが目的。