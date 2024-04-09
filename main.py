from fastapi import FastAPI, Request
from requests import post, get
from dotenv import load_dotenv
from os import getenv
from uvicorn import run

load_dotenv()

CHAT_ID = getenv("CHAT_ID")
BOT_TOKEN = getenv("BOT_TOKEN")
VERCEL_URL = getenv("VERCEL_URL")

url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={VERCEL_URL}/telebot"
response = get(url)

# Initialize the FastAPI app
app = FastAPI()


async def send_message(chat_id, text):
    """
    Send a message to a Telegram chat via the Telegram Bot API.

    Parameters:
        chat_id (str): The chat ID to send the message to.
        text (str): The message to send.
    """
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    await post(api_url, json=params)


@app.post("/telebot")
async def webhook(request: Request):
    """
    Handle incoming webhook from Telegram

    If the POST request contains a message, then we process it,
    otherwise we process an edited message.
    """
    data = await request.json()
    if "message" in data:
        message_type = "message"
    else:
        message_type = "edited_message"

    # Get the chat ID and the message text
    chat_id = data[message_type]["chat"]["id"]
    message_text = data[message_type]["text"]

    # Send the message to the chat
    await send_message(chat_id, message_text)

    # Return a successful response
    return {"message": "OK"}

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)