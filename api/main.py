from logging import getLogger, basicConfig, INFO
from fastapi import FastAPI, Request
from requests import post, get
from dotenv import load_dotenv
from os import getenv
from uvicorn import run

# Load environment variables
load_dotenv()

# Set up logging
basicConfig(level=INFO)
logger = getLogger(__name__)

# Constants from environment variables
CHAT_ID = getenv("CHAT_ID")
BOT_TOKEN = getenv("BOT_TOKEN")
VERCEL_URL = getenv("VERCEL_URL")

# Set up webhook
url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={VERCEL_URL}/telebot"
response = get(url)

# Initialize the FastAPI app
app = FastAPI()

# Function to send message to Telegram
async def send_message(chat_id, text):
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    await post(api_url, json=params)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Telegram Bot"}

# Webhook endpoint
@app.post("/telebot")
async def webhook(request: Request):
    data = await request.json()
    if "message" in data:
        message_type = "message"
    else:
        message_type = "edited_message"
    chat_id = data[message_type]["chat"]["id"]
    message_text = data[message_type]["text"]
    
    # Log incoming message
    logger.info(f"Incoming message: {message_text}")

    # Send message to chat
    await send_message(chat_id, message_text)

    # Return a successful response
    return {"message": "OK"}

# Run the FastAPI app
if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
