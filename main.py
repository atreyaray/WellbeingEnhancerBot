import logging
import os
import pymongo
import requests
from settings import DATABASE_PASSWORD
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, User
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
TG_API_TOKEN = "1313840578:AAG-42QA06vXnRAjpkPgHweyVaaUoGpM4NM"
complete_uri = f'mongodb+srv://teamstemboys:{DATABASE_PASSWORD}@cluster0.aakcb.mongodb.net/<dbname>?retryWrites=true&w=majority'
client = pymongo.MongoClient(complete_uri)
db = client.test
users = db.customers
# Enable Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Stages
CHOICE, WHENSLEEP,WHENSTRESSED, WHENSTUDY = range(4)
# Callback data
SLEEP, STUDYING, STRESSED = range(3)


# Define a few command handlers
def start(update, context):


    """Send a message when the command /start is issued"""
    # update.message.reply_text("Hello world!\nTODO:Enter captivating statement, false promises, and high hopes.")

    # The keyboard is a list of button rows, where each row is a list
    keyboard = [
        [InlineKeyboardButton("Sleeping 😴", callback_data=str(SLEEP)),
         InlineKeyboardButton("Studying 🧠", callback_data=str(STUDYING)),
         InlineKeyboardButton("I'm stressed!!! 😪", callback_data=str(STRESSED)) ]
    ]
    # keyboard = [
    #     [KeyboardButton("Sleep more"),
    #      KeyboardButton("Reduce Smoking")
    #      ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send message with text and appended InlineKeyboard
    update.message.reply_text(
        "❓❓❓Which habit do you want to work on❓❓❓",
        reply_markup=reply_markup
    )
    # TEll ConversationHandler that we're in state 'CHOICE' now
    return CHOICE
    ## Future Reference
    # user = update.message.from_user {Get user - can obtain his/her details through this object}


def stressed(update, context):
    query = update.callback_query
    query.answer()
    query.message.reply_text(
        text=("No problem ♥️")
    )
    keyboard = [
        [InlineKeyboardButton("Lo-fi 🎧", callback_data=str(0)),
         InlineKeyboardButton("Pop 🎤", callback_data=str(1)),
         InlineKeyboardButton("Classical 🎻", callback_data=str(2)),
         InlineKeyboardButton("Rock 🎸", callback_data=str(3))
         ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(
        text="What music would you like? 🎼",
        reply_markup=reply_markup
    )
    return WHENSTRESSED


def when_stressed(update, context):
    """When the user went to sleep"""
    query = update.callback_query
    query.answer()
    link = ['https://www.youtube.com/watch?v=tgI6PjEq0O8',
            'https://www.youtube.com/watch?v=GnivKpaOE24&list=RDCLAK5uy_nmS3YoxSwVVQk9lEQJ0UX4ZCjXsW_psU8&start_radio=1',
            'https://www.youtube.com/watch?v=nJDQMyHbSko&list=PLEF4FCEA775F67968',
            'https://www.youtube.com/watch?v=fJ9rUzIMcZQ&list=PLNxOe-buLm6cz8UQ-hyG1nm3RTNBUBv3K']
    query.message.reply_text(
        text="Here's some music we think you would like "+ link[int(query.data)]
    )
    return CHOICE  # TODO


def sleep(update, context):
    """Show new choice of buttons"""
    query = update.callback_query
    user_id = update.callback_query.message.chat.id
    username = update.callback_query.message.chat.username
    update_id = update.update_id
    first_name = update.callback_query.message.chat.first_name
    last_name = update.callback_query.message.chat.last_name
    users.insert_one({"first_name": first_name, "last_name": last_name, "tg_id": user_id,
                      "last_update": update_id, "sleep": 0})
    query.answer()
    query.message.reply_text(
        text=("Good choice. Let's track your sleep for a couple weeks, and see the trends. 📊")
    )

    keyboard = [
        [InlineKeyboardButton("< 5 hours 😱", callback_data=str(0)),
         InlineKeyboardButton("5-6 hours 😌", callback_data=str(1)),
         InlineKeyboardButton("7-9 hours 😃", callback_data=str(2)),
         InlineKeyboardButton("> 9 hours 🤪", callback_data=str(3))
         ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(
        text="How much did you sleep today? 💤",
        reply_markup=reply_markup
    )
    # query.edit_message_text(
    #     text="First CallbackQueryHandler, Choose a route",
    #     reply_markup=reply_markup
    # )
    return WHENSLEEP

def when_sleep(update, context):
    """When the user went to sleep"""

    query = update.callback_query
    query.answer()
    msg = ['less than 5 hours to sleep. You can spend some more time to sleep!💜',
            "5-6 hours to sleep. That's good!💜" ,
            '7-9 hours to sleep, which is the ideal amount of time one should spend for this activity!💜',
            'more than 10 hours to sleep. Has your alarm been broken?💜']
    
    query.message.reply_text(
        text="💜Awesome! You have spent " + msg[int(query.data)]
    )
    user_id = update.callback_query.message.chat.id
    update_id = update.update_id
    users.update_one(
        {"tg_id": user_id}, {"$set": {"last_update": update_id, "sleep": query.data}})

    return CHOICE # TODO

def study(update, context):
    

    query = update.callback_query
    user_id = update.callback_query.message.chat.id
    username = update.callback_query.message.chat.username
    update_id = update.update_id
    first_name = update.callback_query.message.chat.first_name
    last_name = update.callback_query.message.chat.last_name
    users.insert_one({"first_name": first_name, "last_name": last_name, "tg_id": user_id,
                      "last_update": update_id, "sleep": 0}) 
    query.answer()
    query.message.reply_text(
        text=("Hey! Let's keep track your study timing to see how hard you work! 📚")
    )

    keyboard = [
        [InlineKeyboardButton("< 1 hour 😩", callback_data=str(0)),
         InlineKeyboardButton("2-4 hours 😁", callback_data=str(1)),
         InlineKeyboardButton("5-7 hours 🤓", callback_data=str(2)),
         InlineKeyboardButton("> 7 hours 🤯", callback_data=str(3))
         ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(
        text="How much time did you spend for studying today? 🎯",
        reply_markup=reply_markup
    )
    # query.edit_message_text(
    #     text="First CallbackQueryHandler, Choose a route",
    #     reply_markup=reply_markup
    # )
    return WHENSTUDY

def when_study(update, context):
    """When the user went to sleep"""

    query = update.callback_query
    query.answer()
    msg = [' less than 1 hour to study. It is recommended that one should spend at least 2 hours perday to study.💜',
            " 2-4 hours to study. This is a very ideal amount for studying! Keep up the good work!💜" ,
            " 5-7 hours to study. Wow! You're working very hard! You're gonna ace this period!💜",
            " more than 7 hours to study! Don't forget to spend time for yourself💜"]
    
    query.message.reply_text(
        text= "💜You have spent" + msg[int(query.data)]
    )
    user_id = update.callback_query.message.chat.id
    update_id = update.update_id
    users.update_one(
        {"tg_id": user_id}, {"$set": {"last_update": update_id, "sleep": query.data}})

    return CHOICE # TODO

def end(update, context):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="See you next time!"
    )
    return ConversationHandler.END


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
    # dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # Setup conversation handler with the states CHOICE and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOICE: [CallbackQueryHandler(sleep, pattern='^' + str(SLEEP) + '$'), # Will show differnt durations
                     CallbackQueryHandler(study, pattern='^' + str(STUDYING) + '$'),
                     CallbackQueryHandler(stressed, pattern='^' + str(STRESSED) + '$')],
            WHENSTUDY: [CallbackQueryHandler(when_study)],
            WHENSLEEP: [CallbackQueryHandler(when_sleep)],
            WHENSTRESSED: [CallbackQueryHandler(when_stressed)]

        },
        fallbacks=[CommandHandler('start', start)]
    )

    # On noncommand i.e. message -echo the message on telegram TODO for now
    # dp.add_handler(MessageHandler(Filters.text, echo))
    # Add ConversationHandler to dispatcher that will be used for handling
    # updates
    dp.add_handler(conv_handler)

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
