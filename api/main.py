from requests import post
from flask import Flask, request
from dotenv import load_dotenv
from os import getenv

load_dotenv()


app = Flask(__name__)

BOT_TOKEN = getenv("BOT_TOKEN")
BOT_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_message(answer):
    post(url=f"{BOT_URL}/sendMessage", json=answer)


def get_answer(data):
    chat_id = data["message"]["chat"]["id"]
    message = data["message"]["text"]
    answer = {
        "chat_id": chat_id,
        "text": message,
    }
    return answer


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    answer = get_answer(data)
    send_message(answer)
    return "Message sent"


@app.route("/")
def index():
    return "Bot is running"
