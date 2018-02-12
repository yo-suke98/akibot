# -*- encoding: utf-8 -*-
import json
import random
import requests

from django.shortcuts import render
from django.http import HttpResponse

from load_serif import aki_serif  # 先ほどのセリフ一覧をimport

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = 'F3xd5MjZfyz0gOj14L4WEBYGgk7We4AEpmLNPL/ORfcLqzkY/8+cMi9KnAXEhELF4/GwstVwbV6ISqyFvpR3aMv2P0epfGoCZEfSRh727SSO5z7pTRjkvCGOmHf9bmbpzwIOWO67y6Y+xSJx2dBdhAdB04t89/1O/w1cDnyilFU='
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN
}

def index(request):
    return HttpResponse("This is bot api.")

def reply_text(reply_token, text):
    reply = random.choice(aki_serif)
    payload = {
          "replyToken":reply_token,
          "messages":[
                {
                    "type":"text",
                    "text": reply
                }
            ]
    }

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload)) # LINEにデータを送信
    return reply

def callback(request):
    reply = ""
    request_json = json.loads(request.body.decode('utf-8')) # requestの情報をdict形式で取得
    for e in request_json['events']:
        reply_token = e['replyToken']  # 返信先トークンの取得
        message_type = e['message']['type']   # typeの取得

        if message_type == 'text':
            text = e['message']['text']    # 受信メッセージの取得
            reply += reply_text(reply_token, text)   # LINEにセリフを送信する関数
    return HttpResponse(reply)  # テスト用
