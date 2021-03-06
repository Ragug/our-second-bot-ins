import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from traceback import format_exc
from instaloader import Instaloader, Profile
import time
from consts import *
import re


'''made by RAGU G 😃😃😃😃'''


L = Instaloader()
TOKEN = os.getenv("BOT_TOKEN")
APP_NAME = os.getenv("APP_NAME")
TELEGRAM_USERNAME = os.getenv("TELEGRAM_USERNAME")

mediaregpat = r"(https?:\/\/(?:www\.)?instagram\.com\/(?:p|reel|tv)\/([^\/?#&\n]+)).*"
proregpat = r"(https?:\/\/(?:www\.)?instagram\.com\/([a-z1-9_\.?=]+)).*"


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

import pyrogram
from pyrogram import Client, Filters, StopPropagation, InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(Filters.command(["start"]), group=-2)
async def start(client, message):
    # return
    joinButton = InlineKeyboardMarkup([
        [InlineKeyboardButton("Channel", url="https://t.me/aryan_bots")],
        [InlineKeyboardButton(
            "Report Bugs 😊", url="https://t.me/aryanvikash")]
    ])
    welcomed = f"Hey <b>{message.from_user.first_name}</b>\n/help for More info"
    await message.reply_text(welcomed, reply_markup=joinButton)
    raise StopPropagation


def help_msg(update, context):
    update.message.reply_text("Send Any instagram users username(without @) or their profile url to get their profile pricture")


def contact(update, context):
    keyboard = [[InlineKeyboardButton(
        "Contact", url=f"telegram.me/{TELEGRAM_USERNAME}")], ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Contact The Maker:', reply_markup=reply_markup)

# get the username and send the DP


def username(update, context):
    query = update.message.text

    if not re.compile(mediaregpat).search(query):
        msg = update.message.reply_text("Downloading...")
        if re.compile(proregpat).search(query):
            query = get_username(query)
        chat_id = update.message.chat_id
        try:
            user = Profile.from_username(L.context, query)
            caption_msg = create_caption(user)
            context.bot.send_photo(
                chat_id=chat_id, photo=user.profile_pic_url,
                caption=caption_msg, parse_mode='MarkdownV2')
            update.message.reply_text("You can get telegram stickers click below button 😃",
                                      reply_markup=InlineKeyboardMarkup(ratingkey))
            msg.edit_text("finished.")
            time.sleep(5)
        except Exception as e:
            print(format_exc())
            msg.edit_text("Try again 😕😕 Check the username correctly")
    else:
        update.message.reply_html("This bot only supports downloading of Profile picture please do not send media url.")


def source(update, context):
    update.message.reply_text("RG-bots")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        TOKEN, use_context=True)
    PORT = int(os.environ.get('PORT', '8443'))
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_msg))
    dp.add_handler(CommandHandler("contact", contact))
    dp.add_handler(CommandHandler("source", source))
    dp.add_handler(MessageHandler(Filters.text, username, run_async=True))
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot

    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN,webhook_url=f"https://{APP_NAME}.herokuapp.com/" + TOKEN, drop_pending_updates=True)
    #updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
