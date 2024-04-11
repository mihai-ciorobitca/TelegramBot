from fastapi import FastAPI, Request 
from requests import post, get
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = FastAPI()

BOT_TOKEN = getenv("BOT_TOKEN")
BOT_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
WEBHOOK_URL = f"{BOT_URL}/setwebhook?url=https://mihai-telegram-bot.vercel.app/webhook"

 

def send_message(answer):
    post(url=f"{BOT_URL}/sendMessage", json=answer)


def get_answer(data: dict):
    chat_id = data["message"]["chat"]["id"]
    message = data["message"]["text"]
    answer = {
        "chat_id": chat_id,
        "text": message,
    }
    return answer


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    answer = get_answer(data)
    send_message(answer)
    return {"message": "Message sent"}


@app.get("/")
async def index():
    response = get(url=WEBHOOK_URL)
    return response.json()
