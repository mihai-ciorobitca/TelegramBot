from telegram.ext import Updater, CommandHandler
from os import getenv
from dotenv import load_dotenv

load_dotenv()

def start(update, context):
    update.message.reply_text('Hello! I am your Telegram bot.')

def help(update, context):
    update.message.reply_text('You can use /start to begin and /help to get assistance.')

def handler(event, context):
    # Initialize bot
    updater = Updater(getenv('BOT_TOKEN'), use_context=True)
    dp = updater.dispatcher

    # Register handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()
