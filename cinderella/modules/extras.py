import random
from telegram.ext import run_async, Filters
from telegram import Message, Chat, Update, Bot, MessageEntity
from cinderella import dispatcher
from cinderella.modules.disable import DisableAbleCommandHandler

ABUSE_STRINGS = (
    "Teri Maa ka Bhonsda",
    "You are a gay like divine",
    "Oye BSDK, Teri Gand me sariya paake garam kardunga...",
    "Come on Get Your Mother Raped By Me",
    "Aja mera lund chaatle",
    "teri maa ka rape karke tujhe paida kia tha bete",
    "andi bandi sandi...agar tune apna account delete na kia to teri maa randi..."
  )


@run_async
def abuse(bot: Bot, update: Update):
    bot.sendChatAction(update.effective_chat.id, "typing") # Bot typing before send messages
    message = update.effective_message
    if message.reply_to_message:
      message.reply_to_message.reply_text(random.choice(ABUSE_STRINGS))
    else:
      message.reply_text(random.choice(ABUSE_STRINGS))

__help__ = """
This is a module for extra commands either funny or serious ones....

*Commands:*
- /abuse : To Abuse Someone.

"""

__mod_name__ = "Extras"

ABUSE_HANDLER = DisableAbleCommandHandler("abuse", abuse)


dispatcher.add_handler(ABUSE_HANDLER)

