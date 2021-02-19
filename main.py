from flask import Flask, request, abort
import json
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from linebot.exceptions import LineBotApiError
import os
import getter as g

# heroku上では使わない
# localで動かすときは必要
# from dotenv import load_dotenv
# load_dotenv()

app = Flask(__name__)

# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == 'GPA':
        gpa = g.calcGPA()
        message = "あなたのGPAは " + str(gpa)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='計測中…'))

        # userIdを取得する場合はcheck()をコメントアウトしてください
        check()

        # userIdを取得する場合は以下のコメントアウトを外してください
        # message = 'IDtest'
        # # userIdを取得
        # userId = json.loads(str(event.source))
        # userId = userId['userId']
        # message += '\n ' + userId
        # line_bot_api.reply_message(
        #     event.reply_token,
        #     TextSendMessage(text=message))


def check():
    flag, updateList = g.run()
    # 更新されたもののリストを取得
    strlist = '\n'.join(updateList)
    message = str()
    gpa = float()
    if flag:
        message = "更新されたよ！\n"
        gpa = g.calcGPA()
        message += '\nあなたのGPAは ' + str(gpa)
    else:
        message = "更新されたものはないよ！"
    # 設定されているuserIDにのみ送信
    USER_ID = os.environ["USER_ID"]
    line_bot_api.push_message(USER_ID, TextSendMessage(text=message + strlist))


if __name__ == "__main__":
    # app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
