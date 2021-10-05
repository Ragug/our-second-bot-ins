from telegram import InlineKeyboardButton
from telegram.utils.helpers import escape_markdown as es




def acc_type(val):
    if(val):
        return "🔒Private🔒"
    else:
        return "🔓Public🔓"


def create_caption(user):
    caption_msg = f'''📛*Name*📛: {es(user.full_name,version=2)} \n😁*Followers*😁: {es(str(user.followers),version=2)} \n🤩*Following*🤩: {es(str(user.followees),version=2)}\
        \n🧐*Account Type*🧐: {acc_type(user.is_private)} \n\nThank You For Using The bot 😀😀'''

    return caption_msg


def get_username(url):
    try:
        data = url.split("/")[3]
        if "?" in data:
            try:
                data = data.split("?")
                return data[0]
            except Exception:
                return "incorrect format"
        return data
    except Exception:
        return "incorrect format"


ratingkey = [[InlineKeyboardButton(
    "Telegram Stickers", url="https://t.me/RG_bots/63")]]
