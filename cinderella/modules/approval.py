from cinderella.modules.disable import DisableAbleCommandHandler
from cinderella import dispatcher, SUDO_USERS, telethn
from cinderella.modules.helper_funcs.extraction import extract_user
from telegram.ext import run_async
import cinderella.modules.sql.approve_sql as sql
from cinderella.modules.helper_funcs.chat_status import (bot_admin, user_admin)
from cinderella.modules.helper_funcs.alternate import typing_action
from telegram import ParseMode
from telegram import Update, Bot, Message, Chat, User
from telethon import events, Button
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantCreator
from typing import Optional, List


async def is_administrator(user_id: int, message):
    admin = False
    async for user in message.client.iter_participants(
        message.chat_id, filter=ChannelParticipantsAdmins
    ):
        if user_id == user.id or user_id in SUDO_USERS:
            admin = True
            break
    return admin

async def c(event):
   msg = 0
   async for x in event.client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    if isinstance(x.participant, ChannelParticipantCreator):
       msg += x.id
   return msg

@user_admin
@run_async
def approve(bot: Bot, update: Update, args: List[str]) -> str:
	 message = update.effective_message
	 chat_title = message.chat.title
	 chat = update.effective_chat
	 
	 user_id = extract_user(message, args)
	 if not user_id:
	     message.reply_text("I don't know who you're talking about, you're going to need to specify a user!")
	     return ""
	 member = chat.get_member(int(user_id))
	 if member.status == "administrator" or member.status == "creator":
	     message.reply_text(f"User is already admin - locks, blocklists, and antiflood already don't apply to them.")
	     return
	 if sql.is_approved(message.chat_id, user_id):
	     message.reply_text(f"[{member.user['first_name']}](tg://user?id={member.user['id']}) is already approved in {chat_title}", parse_mode=ParseMode.MARKDOWN)
	     return
	 sql.approve(message.chat_id, user_id)
	 message.reply_text(f"[{member.user['first_name']}](tg://user?id={member.user['id']}) has been approved in {chat_title}! They will now be ignored by automated admin actions like locks, blocklists, and antiflood.", parse_mode=ParseMode.MARKDOWN)
     
@user_admin
@run_async
def disapprove(bot: Bot, update: Update, args: List[str]) -> str:
	 message = update.effective_message
	 chat_title = message.chat.title
	 chat = update.effective_chat
	 
	 user_id = extract_user(message, args)
	 if not user_id:
	     message.reply_text("I don't know who you're talking about, you're going to need to specify a user!")
	     return ""
	 member = chat.get_member(int(user_id))
	 if member.status == "administrator" or member.status == "creator":
	     message.reply_text("This user is an admin, they can't be unapproved.")
	     return
	 if not sql.is_approved(message.chat_id, user_id):
	     message.reply_text(f"{member.user['first_name']} isn't approved yet!")
	     return
	 sql.disapprove(message.chat_id, user_id)
	 message.reply_text(f"{member.user['first_name']} is no longer approved in {chat_title}.")
     
@user_admin
@run_async
def approved(bot: Bot, update: Update, args: List[str]) -> str:
    message = update.effective_message
    chat_title = message.chat.title
    chat = update.effective_chat
    no_users = False
    msg = "The following users are approved.\n"
    x = sql.list_approved(message.chat_id)
    for i in x:
        try:
            member = chat.get_member(int(i.user_id))
        except:
            pass
        msg += f"- `{i.user_id}`: {member.user['first_name']}\n"
    if msg.endswith("approved.\n"):
      message.reply_text(f"No users are approved in {chat_title}.")
      return
    else:
      message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

@user_admin
@run_async
def approval(bot: Bot, update: Update, args: List[str]) -> str:
	 message = update.effective_message
	 chat = update.effective_chat
	 
	 user_id = extract_user(message, args)
	 member = chat.get_member(int(user_id))
	 if not user_id:
	     message.reply_text("I don't know who you're talking about, you're going to need to specify a user!")
	     return ""
	 if sql.is_approved(message.chat_id, user_id):
	     message.reply_text(f"{member.user['first_name']} is an approved user. Locks, antiflood, and blocklists won't apply to them.")
	 else:
	     message.reply_text(f"{member.user['first_name']} is not an approved user. They are affected by normal commands.")

@run_async
@bot_admin
@user_admin
@typing_action
def unapproveall(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat 
    user = update.effective_user 
    message = update.effective_message
    chat_id = str(chat.id)[1:] 
    approve_list = list(REDIS.sunion(f'approve_list_{chat_id}'))
    for target_user in approve_list:
        REDIS.srem(f'approve_list_{chat_id}', target_user)
    message.reply_text(
        "Successully unapproved all users from {}.".format(chat.title)
    )

			
				
__help__  = """
Sometimes, you might trust a user not to send unwanted content.
Maybe not enough to make them admin, but you might be ok with locks, blacklists, and antiflood not applying to them.

That's what approvals are for - approve of trustworthy users to allow them to send 

*Admin commands:*
- `/approval`*:* Check a user's approval status in this chat.
- `/approve`*:* Approve of a user. Locks, blacklists, and antiflood won't apply to them anymore.
- `/unapprove`*:* Unapprove of a user. They will now be subject to locks, blacklists, and antiflood again.
- `/approved`*:* List all approved users.
- `/unapproveall`*:* Unapprove *ALL* users in a chat. This cannot be undone.
"""

APPROVE = DisableAbleCommandHandler("approve", approve, pass_args=True)
DISAPPROVE = DisableAbleCommandHandler("unapprove", disapprove, pass_args=True)
LIST_APPROVED = DisableAbleCommandHandler("approved", approved, pass_args=True)
APPROVAL = DisableAbleCommandHandler("approval", approval, pass_args=True)

dispatcher.add_handler(APPROVE)
dispatcher.add_handler(DISAPPROVE)
dispatcher.add_handler(LIST_APPROVED)
dispatcher.add_handler(APPROVAL)

__mod_name__ = "Approval"
__command_list__ = ["approve", "unapprove", "approved", "approval"]
__handlers__ = [APPROVE, DISAPPROVE, APPROVAL]
