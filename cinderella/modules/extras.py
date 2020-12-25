import random
from telegram.ext import run_async, RegexHandler, Filters
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

SOURCE_STRINGS = (
    "Source ka kya karega madarchod😒",
    "Ek dunga, Source ka naam bhi nhi lega fir😠",
    "Hack Github and Make my Repo Public, If you want my source🤣",
    "Lund lele source ki jagah🖕",
    "💩Tatti Khaale, Aya Bada Source Maangne Wala",
    "The Person who asks for My Source is a Gay😒😒😒",
    "Fuck Yourself Before Asking For Source"
  )

ANONY_STRINGS = (
    "Anony ko kyu tag kia madarchod😒",
    "Don't dare to tag my owner."
  )



@run_async
def abuse(bot: Bot, update: Update):
    bot.sendChatAction(update.effective_chat.id, "typing") # Bot typing before send messages
    message = update.effective_message
    if message.reply_to_message:
      message.reply_to_message.reply_text(random.choice(ABUSE_STRINGS))
    else:
      message.reply_text(random.choice(ABUSE_STRINGS))
    
@run_async
def source(bot: Bot, update: Update):
    bot.sendChatAction(update.effective_chat.id, "typing") # Bot typing before send messages
    message = update.effective_message
    if message.reply_to_message:
      message.reply_to_message.reply_text(random.choice(SOURCE_STRINGS))
    else:
      message.reply_text(random.choice(SOURCE_STRINGS))
    
@run_async
def anonyindian(bot: Bot, update: Update):
    bot.sendChatAction(update.effective_chat.id, "typing") # Bot typing before send messages
    message = update.effective_message
    if message.reply_to_message:
      message.reply_to_message.reply_text(random.choice(ANONY_STRINGS))
    else:
      message.reply_text(random.choice(ANONY_STRINGS))
    
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
- /wiki `<query>`: Wiki your query.

"""

__mod_name__ = "Extras"

ABUSE_HANDLER = DisableAbleCommandHandler("abuse", abuse)
SOURCE_HANDLER = DisableAbleCommandHandler("source", source)
OWNER_TAG_HANDLER = RegexHandler("(?i)@anonyindian(s)?", anonyindian)

dispatcher.add_handler(ABUSE_HANDLER)
dispatcher.add_handler(SOURCE_HANDLER)
dispatcher.add_handler(OWNER_TAG_HANDLER)
