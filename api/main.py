from requests import post
from flask import Flask, request
from dotenv import load_dotenv
from os import getenv
from logging import basicConfig, ERROR, error, exception

load_dotenv()

basicConfig(filename='error.log', level=ERROR)

app = Flask(__name__)

BOT_TOKEN = getenv("BOT_TOKEN")
BOT_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_message(prepared_data):
    response = post(url=f"{BOT_URL}/sendMessage", json=prepared_data)
    return response.status_code


def get_answer(data):
    chat_id = data["message"]["chat"]["id"]
    message = data["message"]["text"]
    answer = message  # echo message
    json_data = {
        "chat_id": chat_id,
        "text": answer,
    }
    return json_data


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        answer = get_answer(data)
        status = send_message(answer)
        if status == 200:
            return "Message sent"
        else:
            error("Failed to send message")
            return "An error occurred while sending the message", 500
    except Exception as e:
        exception(f"An error occurred: {e}") 
        return "An unexpected error occurred", 500


@app.route("/")
def index():
    return "Bot is running"
