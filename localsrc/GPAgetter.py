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
#options.add_argument('--headless')  # ※ヘッドレスモードを使用する場合、コメントアウトを外す

#
# Chromeドライバーの起動
#
driver = webdriver.Chrome(chrome_options=options)

driver.implicitly_wait(10)  # 秒

#
#
# クローリング/スクレイピング
#
#

# 学情にアクセスする
url = os.environ['URL']
driver.get(url)

# トップページでログインボタンを押す
selector = '#left_container > div.left-module-top.bg_color > div > div > a'
element = driver.find_element_by_css_selector(selector)
driver.execute_script('arguments[0].click();', element)

# username
selector = '#username'
element = driver.find_element_by_css_selector(selector)
element.send_keys(MY_ID)

# password
selector = '#password'
element = driver.find_element_by_css_selector(selector)
element.send_keys(MY_PASS)

# Loginボタン
selector = 'body > div > div > div > div > form > div:nth-child(3) > button'
element = driver.find_element_by_css_selector(selector)
driver.execute_script('arguments[0].click();', element)

# 教務システム
selector = '#home_systemCooperationLink > div.left-module.mt15 > div > ul > li:nth-child(1) > a'
element = driver.find_element_by_css_selector(selector)
driver.execute_script('arguments[0].click();', element)

# ウィンドウハンドルを取得する
handle_array = driver.window_handles
# 一番最後のdriverに切り替える
driver.switch_to.window(handle_array[-1])


# 成績情報の参照
selector = 'body > table:nth-child(4) > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table > tbody > tr:nth-child(1) > td:nth-child(2) > a'
element = driver.find_element_by_css_selector(selector)
driver.execute_script('arguments[0].click();', element)

# ウィンドウハンドルを取得する
handle_array = driver.window_handles
# 一番最後のdriverに切り替える
driver.switch_to.window(handle_array[-1])

# while(True):

# 学科等案内GPA
selector = 'body > table:nth-child(8) > tbody > tr > td:nth-child(2) > table > tbody > tr > td:nth-child(5) > span > img'
element = driver.find_element_by_css_selector(selector)
driver.execute_script('arguments[0].click();', element)

# ウィンドウハンドルを取得する
handle_array = driver.window_handles
# 一番最後のdriverに切り替える
driver.switch_to.window(handle_array[-1])

# 累計GPA
selector = 'body > table:nth-child(3) > tbody > tr > td > table > tbody > tr:nth-child(2) > td:nth-child(2)'
element = driver.find_element_by_css_selector(selector)
# GPA出力
print("Your GPA is " + element.text)

# 戻る処理
selector = 'body > table:nth-child(5) > tbody > tr > td > table > tbody > tr > td > input[type=image]'
element = driver.find_element_by_css_selector(selector)
driver.execute_script('arguments[0].click();', element)

# ウィンドウハンドルを取得する
handle_array = driver.window_handles
# 一番最後のdriverに切り替える
driver.switch_to.window(handle_array[-1])


time.sleep(10)
driver.quit()
