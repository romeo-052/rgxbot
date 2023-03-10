import telepot
import re
import os
import random
import string
import time
from flask import Flask, render_template, session, url_for, redirect, request
from telepot.namedtuple import *

import requests
username = 'romeoxD'
token = '399d331f954b2685c9532224f79538df378aa036'

response = requests.get(
    'https://www.pythonanywhere.com/api/v0/user/{username}/cpu/'.format(
        username=username
    ),
    headers={'Authorization': 'Token {token}'.format(token=token)}
)
if response.status_code == 200:
    print('CPU quota info:')
    print(response.content)
else:
    print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))
                        
telepot.api.set_proxy('http://proxy.server:3128')
bot = telepot.Bot(5882355812:AAFrCVfieKhyq5K2-eCupxDdI5jq5VzXaks)
bot.setWebhook(URL, max_connections=10)

def processing(msg):
    if 'chat' in msg and msg['chat']['type'] == 'channel':
        return
        
    id = msg['from']['id']
    
    if 'text' in msg:
        msg['text'] = str(msg['text']) # FEELING SAFER ;)
        msg['type'] = 'text'

    elif 'data' in msg:
        msg['type'] = 'callback'
        msg['text'] = f"%callback {msg['data']}"

    else:
        msg['type'] = 'nontext'
        types = ['audio', 'voice', 'document', 'photo',
                 'video', 'contact', 'location']

        for type in types:
            if type in msg:
                msg['text'] = f'%{type}'
                break

    if 'text' in msg:
        for entry in regex:
            if re.match(entry, msg["text"]):
                matches = re.match(entry, msg["text"]).groups()
                parser(msg, list(matches))
                return


app = Flask(__name__)

@app.route(f'/{SECRET}', methods=["POST"])
def webhook():
    update = request.get_json()
    if "message" in update:
        processing(update['message'])

    elif 'callback_query' in update:
        processing(update['callback_query'])

    return 'OK'

regex = [
    r'^[!/](start)',
    r'^[!/](echo) (.*)'
]

def parser(msg, matches):
    usr = msg['from']

    if msg['type'] == "text":
        if matches[0] == 'start':
            text = "welcome message"
            markup = InlineKeyboardMarkup(inline_keyboard=[
                                [InlineKeyboardButton(text='BTN1', callback_data='btn1'),
                                InlineKeyboardButton(text='BTN2', callback_data='btn2')]
                        ])

            bot.sendMessage(usr['id'], text, reply_markup=markup)
            return

        if matches[0] == 'echo' and matches[1]:
            bot.sendMessage(usr['id'], matches[1])
            return

if __name__ == "__main__":
    app.run()
