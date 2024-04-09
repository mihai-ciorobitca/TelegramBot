from fastapi import FastAPI, Request # to create the FastAPI app 
from requests import post # to send the POST request
from dotenv import load_dotenv # to load the .env file
from os import getenv # to get the token from the .env file

load_dotenv() # load the .env file

CHAT_ID = getenv("ID") # get the chat ID from the .env file
TOKEN = getenv("TOKEN") # get the token from the .env file

# Initialize the Flask app
app = FastAPI()


def send_message(chat_id, text):
    """
    Send a message to a Telegram chat via the Telegram Bot API.

    Parameters:
        chat_id (str): The chat ID to send the message to.
        text (str): The message to send.
    """
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    post(api_url, json=params)


@app.post("/telebot") 
async def webhook(request: Request):
    """
    Handle incoming webhook from Telegram

    If the POST request contains a message, then we process it,
    otherwise we process an edited message.
    """
    data = await request.json
    if "message" in data:
        message_type = "message"
    else:
        message_type = "edited_message"

    # Get the chat ID and the message text
    chat_id = data[message_type]["chat"]["id"]
    message_text = data[message_type]["text"]

    # Send the message to the chat
    send_message(chat_id, message_text)

    # Return a successful response
    return {"message": "OK"}
 
