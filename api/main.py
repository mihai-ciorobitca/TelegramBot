from flask import Flask, request
from telebot import TeleBot, types
from dotenv import load_dotenv
from os import getenv

load_dotenv()

VERCEL_URL = getenv('VERCEL_URL')
BOT_TOKEN = getenv('BOT_TOKEN')

# Initialize Flask app
app = Flask(__name__)

# Initialize Telebot with your bot token
bot = TeleBot(BOT_TOKEN)

# Define route for receiving webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    update = types.Update.de_json(request.json)
    bot.process_new_updates([update])
    return '', 200

# Define handler for /start and /help commands
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

# Define handler for all other messages
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Start Flask app
if __name__ == '__main__':
    # Set webhook
    bot.remove_webhook()
    bot.set_webhook(url=f"{VERCEL_URL}/webhook")
    # Run Flask app
    app.run(host="0.0.0.0", port=8000) 
