import sys
import traceback

from functools import wraps
from typing import Optional

from telegram import User, Chat, ChatMember, Update, Bot
from telegram import error

from cinderella import DEL_CMDS, SUDO_USERS, WHITELIST_USERS


def send_message(message, text,  *args,**kwargs):
	try:
		return message.reply_text(text, *args,**kwargs)
	except error.BadRequest as err:
		if str(err) == "Reply message not found":
			return message.reply_text(text, quote=False, *args,**kwargs)
		
def typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(bot: Bot, update: Update, *args, **kwargs):
        bot.sendChatAction(update.effective_chat.id, "typing") 
        return func(bot: Bot, update: Update, *args, **kwargs)

    return command_func
