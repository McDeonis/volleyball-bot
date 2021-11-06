from flask import Flask, request, jsonify
from os.path import join, dirname
from dotenv import load_dotenv
import requests
import os
import json


def get_from_env(key):
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)  # возвращает токен и секретные велечины


app = Flask(__name__)
app.debug = True
token = get_from_env("TOKEN")
telegram_url = get_from_env("TELEGRAM_URL")
heroku_url = get_from_env("HEROKU_URL")
g_sheet = get_from_env("GOOGLE_URL_SHEET")


def send_message(chat_id, text, reply_to_msg_id):
    method = "sendMessage"
    url = f"{telegram_url}{token}/{method}"
    data = {"chat_id": chat_id, "text": text, "reply_to_message_id": reply_to_msg_id}
    return requests.post(url, json=data)


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as req_msg:
        json.dump(data, req_msg, indent=2, ensure_ascii=False)


# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return '<h1>Hello</h1>'


@app.route(f'/'.format(token), methods=["POST"])  # localhost:5000 - на этот адрес телеграмм шлет сообщения
def process():
    write_json(request.json)
    req = request.get_json()
    chat_id = req["message"]["chat"]["id"]
    message = req["message"]["text"]
    message_id = req["message"]["message_id"]
    user_name = req["message"]["from"]["username"]

    if message == "/start":
        bot_welcome = f"Welcome "+user_name+f" to Volleybal bot.\n The bot is using the service to check your workout " \
                                                "status, booking or change you workout days"
        send_message(chat_id=chat_id, text=bot_welcome, reply_to_msg_id='NONE')
        return jsonify(req)
    else:
        send_message(chat_id=chat_id, text="HI", reply_to_msg_id=message_id)
        return {"OK": True}


if __name__ == '__main__':
    app.run()
