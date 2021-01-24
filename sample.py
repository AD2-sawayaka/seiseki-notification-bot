import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from urllib.request import urlopen
import chromedriver_binary

from dotenv import load_dotenv
import os

load_dotenv()
MY_ID = os.environ["MY_ID"]
MY_PASS = os.environ["MY_PASS"]


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
url = 'file:///Users/otyamura/git/seiseki-nortification-bot/html/score.htm'
driver.get(url)

cur_url = driver.current_url

html = urlopen(cur_url)
bsObj = BeautifulSoup(html, "html.parser")

table = bsObj.findAll('table')[-3]
# print(table)
rows = table.select("tr")


# 科目名、担当教員名、科目区分、必修選択区分、単位、評価、得点、科目GP、取得年度、報告日
subject_name = list()
teacher_name = list()
subject_classification = list()
required_selection_category = list()
unit = list()
evaluation = list()
score = list()
GP = list()
acquisition_year = list()
reporting_date = list()

count = 0


for row in rows:
    tmp = list()
    for cell in row.findAll(['td', 'th']):
        tmp.append(cell.get_text(strip=True))
        # print(cell.get_text(strip=True))
    print(tmp)

# # 成績情報の参照
# selector = 'body > table:nth-child(4) > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table > tbody > tr:nth-child(1) > td:nth-child(2) > a'
# element = driver.find_element_by_css_selector(selector)
# driver.execute_script('arguments[0].click();', element)

# # ウィンドウハンドルを取得する
# handle_array = driver.window_handles
# # 一番最後のdriverに切り替える
# driver.switch_to.window(handle_array[-1])

# # while(True):

# # 学科等案内GPA
# selector = 'body > table:nth-child(8) > tbody > tr > td:nth-child(2) > table > tbody > tr > td:nth-child(5) > span > img'
# element = driver.find_element_by_css_selector(selector)
# driver.execute_script('arguments[0].click();', element)

# # tableを取得
# selector = 'body > table:nth-child(10)'
# rows = driver.find_element_by_css_selector(selector)
# for row in rows:
#     print(row)

time.sleep(10)
driver.quit()
