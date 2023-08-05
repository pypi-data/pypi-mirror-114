""" Telegram interface for the bot, using poll method"""

import logging
import os

from telegram import Update, ForceReply
from telegram.error import BadRequest
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from src.config.env import EnvConfig as Config
from src.dataclasses.model import Chat
from src.service.server import Server

# Enable logging
logging.basicConfig(
    format=Config.LOG_FORMAT, level=Config.LOG_LEVEL
)

SERVER = Server()


# Define a few command handlers. These usually take the two arguments update and
# context.
def start_command(update: Update, context: CallbackContext = None) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hallo {user.mention_markdown_v2()}\! Silahkan masukan artikel/topik yang hendak dianalisa',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext = None) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        """📜 Petunjuk penggunaan :
        
Silahkan masukan/forward artikel atau postingan di sini, maka bot akan memulai menganalisa apakah postingan/artikel tersebut mengandung informasi yang valid atau tidak (Hoax). 
Kamu juga bisa masukan topik apapun untuk dianalisa apakah saat ini ada berita atau hoax terkait topik tersebut
        """)


def contact_command(update: Update, context: CallbackContext = None) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("Pertanyaan atau saran bisa hubungi @azzambz")


def handler(update: Update, context: CallbackContext = None) -> None:
    """Method for handling messages"""
    if update.message.text[0] == "!":
        reply = SERVER.magic_keyword(update.message.text)
        update.message.reply_text(reply)
        return

    if update.message.from_user.username:
        sender_id = update.message.from_user.username
    else:
        sender_id = "unknown"
    chat = Chat(
        chat_id=update.message.chat_id,
        sender_id=sender_id,
        sender=update.message.from_user.first_name,
        str_message=update.message.text
    )
    reply = SERVER.handler(chat)
    try:
        logging.debug("Sending message...")
        update.message.reply_text(reply)
    except BadRequest as br:
        logging.error(br)
        update.message.reply_text("Kata/Kalimat terlalu umum, silahkan masukan artikel/topik yang hendak dianalisa!")
    logging.debug("Message sent..")


def start_bot():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    if os.environ.get('BOT_TOKEN'):
        token = os.environ['BOT_TOKEN']
    else:
        logging.error("BOT_TOKEN is not set!")
        return

    updater = Updater(token)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("contact", contact_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handler))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    start_bot()
