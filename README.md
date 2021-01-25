# snipetool

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

.envファイルに以下を参考にIDとパスワードを書いてください

~~~
MY_ID="your id"
MY_PASS="your password"
DATABASE_URL="postgres://postgres:@localhost:5432/seiseki_information"
~~~

DATABASE_URLはここ参照https://qiita.com/hoto17296/items/0ca1569d6fa54c7c4732
