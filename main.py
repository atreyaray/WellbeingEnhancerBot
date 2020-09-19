import logging
import os
from telegram import InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TG_API_TOKEN = "1313840578:AAG-42QA06vXnRAjpkPgHweyVaaUoGpM4NM"
# Enable Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Stages
FIRST, SECOND = range(2)
# Callback data
ONE, TWO, THREE, FOUR = range(4)

# Define a few command handlers
def start(update, context):
    """Send a message when the command /start is issued"""
    update.message.reply_text("Hello world!\nTODO:Enter captivating statement, false promises, and high hopes.")

    # The keyboard is a list of button rows, where each row is a list
    # keyboard = [
    #     [InlineKeyboardButton("1", callback_data=str(ONE)),
    #      InlineKeyboardButton("2", callback_data=str(TWO))]
    # ]

    update.message.reply_text("Please ch")
    ## Future Reference
    # user = update.message.from_user {Get user - can obtain his/her details through this object}



def help(update, context):
    """Send a message when the command /help is issued"""
    update.message.reply_text("Bad Design. Help me fuckers.")


def echo(update, context):
    """Echo the user's message"""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log errors caused by Updates"""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot"""
    # Create the Updater and pass it your bot's token

    updater = Updater(TG_API_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # On different commands, answer in telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # On noncommand i.e. message -echo the message on telegram TODO for now
    dp.add_handler(MessageHandler(Filters.text, echo))

    # Log all errors
    dp.add_error_handler(error)

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. THis should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()