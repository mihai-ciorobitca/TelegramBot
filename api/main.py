import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = "6691717835:AAFPCMjZwI3sUgyYOfz_JcS_3ais3hXCIGs"

BOT_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def get_chat_id(data):
    chat_id = data["message"]["chat"]["id"]
    return chat_id


def get_message(data):
    message_text = data["message"]["text"]
    return message_text


def send_message(prepared_data):
    message_url = BOT_URL + "/sendMessage"
    requests.post(message_url, json=prepared_data)


def change_text_message(text):
    return text[::-1]


def prepare_data_for_answer(data):
    message = get_message(data)
    answer = change_text_message(message)
    chat_id = get_chat_id(data)
    json_data = {
        "chat_id": chat_id,
        "text": answer,
    }
    return json_data


@app.route("/webhook", methods=["POST"])
def post_handler():
    data = request.json
    answer_data = prepare_data_for_answer(data)
    send_message(answer_data)
    return jsonify(success=True)


@app.route("/")
def index():
    return "Hello, World!"
