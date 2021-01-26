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
async def handle_message(event):
    flag, updateList = g.run()
    list = '\n'.join(updateList)
    if flag:
        message = "更新されたよ！\n"
    else:
        message = "更新されたものはないよ！"
    message = 'test'
    await line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='計測中…'))
    # userIdが変化するのであればこれ
    # userId = json.loads(str(event.source))
    # print(userId['userId'])
    # userId = userId['userId']
    userId = 'Ucb74038bc5b24a5a36f6f98b0a470744'
    line_bot_api.push_message(userId, TextSendMessage(text=message))
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=message + list))


if __name__ == "__main__":
    # app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
