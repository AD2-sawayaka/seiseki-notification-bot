import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.request import urlopen
import chromedriver_binary

import psycopg2

from dotenv import load_dotenv
import os


# heroku上では要らない、直接登録して
load_dotenv()
MY_ID = os.environ["MY_ID"]
MY_PASS = os.environ["MY_PASS"]


def get_connection():
    dsn = os.environ.get('DATABASE_URL')
    return psycopg2.connect(dsn)


# Seleniumをあらゆる環境で起動させるChromeオプション
options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--proxy-server="direct://"')
options.add_argument('--proxy-bypass-list=*')
options.add_argument('--start-maximized')
options.add_argument('--headless')  # ※ヘッドレスモードを使用する場合、コメントアウトを外す

#
# Chromeドライバーの起動
#
# DRIVER_PATH = '/Users/otyamura/Desktop/Selenium/chromedriver'
# driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)
driver = webdriver.Chrome(chrome_options=options)

driver.implicitly_wait(10)  # 秒

#
#
# クローリング/スクレイピング
#
#

# 学情にアクセスする
# 適宜置き換えてください
url = 'file:///Users/otyamura/git/seiseki-nortification-bot/html/score.htm'
driver.get(url)

cur_url = driver.current_url

html = urlopen(cur_url)
bsObj = BeautifulSoup(html, "html.parser")

table = bsObj.findAll('table')[-3]
# print(table)
rows = table.select("tr")

# connectionとcursor
conn = get_connection()
cur = conn.cursor()

# 科目名、担当教員名、科目区分、必修選択区分、単位、評価、得点、科目GP、取得年度、報告日
flag = False

for row in rows:
    tmp = list()
    for cell in row.findAll(['td', 'th']):
        if cell.get_text(strip=True) != '':
            text = "'" + cell.get_text(strip=True) + "'"
            text = ''.join(text.split())
            tmp.append(text)
        # print(cell.get_text(strip=True))
    tmp = ', '.join(tmp)
    query = 'INSERT INTO seiseki VALUES (' + tmp + ')'
    if (flag):
        cur.execute(query)
        conn.commit()
    else:
        flag = True


# close
cur.close()
conn.close()

time.sleep(5)
driver.quit()
