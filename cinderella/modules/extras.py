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
- /runs: reply a random string from an array of replies.
- /slap: slap a user, or get slapped if not a reply.
- /shrug : get shrug XD.
- /table : get flip/unflip :v.
- /decide : Randomly answers yes/no/maybe
- /toss : Tosses A coin
- /bluetext : check urself :V
- /roll : Roll a dice.
- /rlg : Join ears,nose,mouth and create an emo ;-;
- /judge: as a reply to someone, checks if they're lying or not!
- /weebify: as a reply to a message, "weebifies" the message.
- /shout `<word>`: shout the specified word in the chat.
- /t: while replying to a message, will reply with a grammar corrected version
- /tr (language code) as reply to a long message.
- /reverse: Does a reverse image search of the media which it was replied to.
- /react: Reacts with a random reaction.

"""

__mod_name__ = "Extras"

ABUSE_HANDLER = DisableAbleCommandHandler("abuse", abuse)


dispatcher.add_handler(ABUSE_HANDLER)

