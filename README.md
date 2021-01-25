# seiseki-nortification-bot

## Usage

GPA出力

~~~
$ python GPAgetter.py
GPAgetter.py:34: DeprecationWarning: use options instead of chrome_options
  driver = webdriver.Chrome(chrome_options=options)
Your GPA is 3.508
~~~

## environment

~~~
$ python -V
Python 3.8.7
~~~

## setup

~~~
pip install selenium
pip install chromedriver_binary
pip install python-dotenv
pip install bs4
pip install psycopg2
pip install flask
pip install line-bot-sdk
~~~

psycopg2のinstallがエラったらこれ
https://dev.classmethod.jp/articles/mac-psycopg2-install/

もしchromeのバージョンが違ったらこのサイトを参考に

http://chromedriver.chromium.org/downloads

~~~
pip install chromedriver_binary==88.hogehoge
~~~

### PostgreSQL

~~~sql
CREATE DATABASE seiseki_information;
\c seiseki_information
\i seiseki.sql
~~~

### env
localで実行する際.envファイルに以下を参考にIDとパスワードを書いてください

~~~
MY_ID="your id"
MY_PASS="your password"
DATABASE_URL="postgres://postgres:@localhost:5432/seiseki_information"
~~~

DATABASE_URLはここ参照https://qiita.com/hoto17296/items/0ca1569d6fa54c7c4732

## Heroku & Line bot

- Line bot作成
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
