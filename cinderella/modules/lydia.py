# AI module using Intellivoid's Coffeehouse API by @TheRealPhoenix
import html
from time import time, sleep
from coffeehouse.lydia import LydiaAI
from coffeehouse.api import API
from coffeehouse.exception import CoffeeHouseError as CFError

from telegram import Message, Chat, User, Update, Bot
from telegram.ext import CommandHandler, MessageHandler, Filters, run_async
from telegram.utils.helpers import mention_html


from cinderella import dispatcher, LYDIA_API, OWNER_ID
from cinderella.modules.helper_funcs.chat_status import user_admin
import cinderella.modules.sql.chatbot_sql as sql
from cinderella.modules.helper_funcs.filters import CustomFilters



CoffeeHouseAPI = API(LYDIA_API)
api_client = LydiaAI(CoffeeHouseAPI)


@run_async
@user_admin
def add_chat(bot: Bot, update: Update):
    global api_client
    chat_id = update.effective_chat.id
    msg = update.effective_message
    user = update.effective_user
    is_chat = sql.is_chat(chat_id)    
    
    
    if not is_chat:
        ses = api_client.create_session()
        ses_id = str(ses.id)
        expires = str(ses.expires)
        sql.set_ses(chat_id, ses_id, expires)
        msg.reply_text("AI CHAT successfully enabled for this chat!")
        message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#AI_ENABLED\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        )
        return message
    else:
        msg.reply_text("AI CHAT is already enabled for this chat!")
        return ""
        
        
        
        
@run_async
@user_admin
def remove_chat(bot: Bot, update: Update):
    msg = update.effective_message
    user = update.effective_user
    chat_id = update.effective_chat.id
    is_chat = sql.is_chat(chat_id)
    if not is_chat:
        msg.reply_text("AI CHAT isn't enabled here in the first place!")
    else:
        sql.rem_chat(chat_id)
        msg.reply_text("AI CHAT disabled successfully!")
        message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#AI_DISABLED\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        )
        return message
        
        
def check_message(bot: Bot, message):
    reply_msg = message.reply_to_message
    if message.text.lower() == "cinderella":
        return True
    if reply_msg:
        if reply_msg.from_user.id == bot.get_me().id:
            return True
    else:
        return False
                
        
@run_async
def lydia(bot: Bot, update: Update):
    global api_client
    msg = update.effective_message
    chat_id = update.effective_chat.id
    is_chat = sql.is_chat(chat_id)
    if not is_chat:
        return
    if msg.text and not msg.document:
        if not check_message(bot, msg):
            return
        sesh, exp = sql.get_ses(chat_id)
        query = msg.text
        try:
            if int(exp) < time():
                ses = api_client.create_session()
                ses_id = str(ses.id)
                expires = str(ses.expires)
                sql.set_ses(chat_id, ses_id, expires)
                sesh, exp = sql.get_ses(chat_id)
        except ValueError:
            pass
        try:
            bot.send_chat_action(chat_id, action='typing')
            rep = api_client.think_thought(sesh, query)
            sleep(0.3)
            msg.reply_text(rep, timeout=60)
        except CFError as e:
            bot.send_message(OWNER_ID, f"lydia error: {e} occurred in {chat_id}!")
            

                    


                  
ADD_CHAT_HANDLER = CommandHandler("eaichat", add_chat, filters=CustomFilters.dev_filter)
REMOVE_CHAT_HANDLER = CommandHandler("daichat", remove_chat, filters=CustomFilters.dev_filter)
LYDIA_HANDLER = MessageHandler(Filters.text & (~Filters.regex(r"^#[^\s]+") & ~Filters.regex(r"^!")
                                  & ~Filters.regex(r"^s\/")), lydia)
# Filters for ignoring #note messages, !commands and sed.

dispatcher.add_handler(ADD_CHAT_HANDLER)
dispatcher.add_handler(REMOVE_CHAT_HANDLER)
dispatcher.add_handler(LYDIA_HANDLER)
