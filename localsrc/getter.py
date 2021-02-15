import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from bs4 import BeautifulSoup
import psycopg2
from dotenv import load_dotenv
import os


def get_connection():
    dsn = os.environ.get('DATABASE_URL')
    return psycopg2.connect(dsn)


# すでに登録されている名前であればTrue
def isResistered(name, cur):
    query = "SELECT subject_name FROM seiseki WHERE subject_name = '" + name +  "'"
    cur.execute(query)
    tmp = str()
    for row in cur:
        tmp = row
    if tmp:
        return True
    return False


def run():
    load_dotenv()
    MY_ID = os.environ["MY_ID"]
    MY_PASS = os.environ["MY_PASS"]
    # chrome driverの配置場所
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
    driver = webdriver.Chrome(chrome_options=options)

    driver.implicitly_wait(3)  # 秒

    # 保存したモノに適宜変更してくださ
    url = 'file:///Users/yourname/seiseki-nortification-bot/html/score.htm'

    driver.get(url)

    # tableを取得
    html = driver.page_source
    bsObj = BeautifulSoup(html, "html.parser")

    table = bsObj.findAll('table')[-3]
    rows = table.select("tr")

    # connectionとcursor
    conn = get_connection()
    cur = conn.cursor()

    # 科目名、担当教員名、科目区分、必修選択区分、単位、評価、得点、科目GP、取得年度、報告日、 試験種別
    flag = False
    update = False
    updateList = list()

    for row in rows:
        tmp = list()
        for cell in row.findAll(['td', 'th']):
            if cell.get_text(strip=True) != '':
                text = "'" + cell.get_text(strip=True) + "'"
                text = ''.join(text.split())
                tmp.append(text)
                # print(cell.get_text(strip=True))
        tmp_name = tmp[0].replace("'", "")
        tmp_str = tmp[0].replace("'", "") + " " + tmp[5].replace("'", "") + " " + tmp[6].replace("'", "")
        # print(tmp_name)
        tmp = ', '.join(tmp)
        if (flag):
            if isResistered(tmp_name, cur):
                print('あるよ')
            else:
                update = True
                print('ないから登録するよ')
                query = 'INSERT INTO seiseki VALUES (' + tmp + ')'
                updateList.append(tmp_str)
                cur.execute(query)
                conn.commit()
        else:
            flag = True
    # close
    cur.close()
    conn.close()

    time.sleep(2)
    driver.quit()
    return update, updateList


if __name__ == '__main__':
    run()
