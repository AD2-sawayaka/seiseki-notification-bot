# seiseki-nortification-bot

## What is it?

これは某大学で使用されている某学務情報システムから成績が更新されたかどうかを通知するLINE botです

## setup

~~~
pip install -r requirements.txt
~~~

psycopg2のinstallがエラったらこれ
https://dev.classmethod.jp/articles/mac-psycopg2-install/

ローカルで実行したい場合は以下も入れてください

~~~
pip install chromedriver_binary
pip install python-dotenv
~~~


もしchromeのバージョンが違ったらこのサイトを参考に

http://chromedriver.chromium.org/downloads

~~~
pip install chromedriver_binary==88.hogehoge
~~~

### PostgreSQL

ローカルのpostgreSQL使うときはこうしてください

~~~sql
CREATE DATABASE seiseki_information;
\c seiseki_information
\i seiseki.sql
~~~

### env
localで実行する際.envファイルに以下を参考に某学情にログインするIDとパスワードを書いてください

~~~
MY_ID="your id"
MY_PASS="your password"
DATABASE_URL="postgres://postgres:@localhost:5432/seiseki_information"
URL="your URL"
~~~

DATABASE_URLはここ参照https://qiita.com/hoto17296/items/0ca1569d6fa54c7c4732

URLは某学務情報システムのurlを入れてください(/portal/ になるように)

## local実行

localsrc内のmain.pyを実行するとLine botのスクリプトが動きます


GPAgetter.pyを動かすと、システムからスクレイピングをしてあなたのGPAをコンソール上に出力してくれます

IDが正しく登録されているかどうかを確認するためにお使いください

getter.pyはローカルに保存した成績情報が記載されているhtmlから成績情報をスクレイピングするスクリプトです

テストにお使いください

ScoreGetter.pyはURLに指定された学情のURLに実際にスクレイピングを行うスクリプトです
LINEに通知はしません


## Heroku & Line bot

- Heroku

~~~
heroku create your-app-name
heroku config:set YOUR_CHANNEL_SECRET="Channel Secretの文字列" --app {自分のアプリケーション名}
heroku config:set YOUR_CHANNEL_ACCESS_TOKEN="アクセストークンの文字列" --app {自分のアプリケーション名}
heroku config:set MY_ID="静大ID" --app {自分のアプリケーション名}
heroku config:set MY_PASS="パスワード" --app {自分のアプリケーション名}
git push heroku main

heroku addons:create heroku-postgresql:hobby-dev -a your_app_name
heroku pg:psql -a your_app_name
=>\i sql/seiseki.sql
=>select * from seiseki;
~~~


- buildpack追加


Buildpack 	URL
chromedrive 	https://github.com/heroku/heroku-buildpack-chromedriver.git

google-chrome 	https://github.com/heroku/heroku-buildpack-google-chrome.git

- Line bot作成

line botを作成した後webhookのURLを

https://app-name.herokuapp.com/callback

にする


### line botの成績を自分にのみ送る方法


誰にでも成績情報が行ってしまうのはまずいので決められたuserIdの人のみにpush通知を送る


~~~python
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = 'IDtest'
    # userIdを取得
    userId = json.loads(str(event.source))
    userId = userId['userId']
    message += '\n ' + userId
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message))
~~~

上記のコードをmain.pyで適切に実行するとuserIdが取得できる

そのあとターミナルで以下を実行
~~~
heroku config:set USER_ID="userIdの文字列" --app {自分のアプリケーション名}
~~~

これで成績情報は自分のアカウントのIDにのみ送信される

## Heroku 定期実行

クレカ登録してから

~~~
heroku addons:add scheduler:standard --app {自分のアプリケーション名}
~~~

herokuのページから
Overview→Heroku Scheduler→Create job

実行するコマンドは
~~~
python check.py
~~~

定期実行する感覚はお好みで
UTCなので日本時間と合わせるには"設定したい時間-9時間"で合わせてください
