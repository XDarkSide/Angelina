from Angelina.modules.disable import DisableAbleCommandHandler
from Angelina import dispatcher, SUDO_USERS, telethn
from Angelina.modules.helper_funcs.extraction import extract_user
from telegram.ext import run_async
import Angelina.modules.sql.approve_sql as sql
from Angelina.modules.helper_funcs.chat_status import (bot_admin, user_admin, promote_permission)
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
@promote_permission
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
@promote_permission
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

@telethn.on(events.CallbackQuery)
async def _(event):
   rights = await is_administrator(event.query.user_id, event)
   creator = await c(event)
   if event.data == b'rmapp':
       if not rights:
             await event.answer("You need to be admin to do this.")
             return
       if creator != event.query.user_id and event.query.user_id not in SUDO_USERS:
             await event.answer("Only owner of the chat can do this.")
             return
       users = []
       x = sql.all_app(event.chat_id)
       for i in x:
          users.append(int(i.user_id))
       for j in users:
           sql.disapprove(event.chat_id, j)
       await event.client.edit_message(event.chat_id, event.query.msg_id, f"Unapproved all users in chat. All users will now be affected by locks, blocklists, and antiflood.")

   if event.data == b'can':
        if not rights:
             await event.answer("You need to be admin to do this.")
             return
        if creator != event.query.user_id and event.query.user_id not in SUDO_USERS:
             await event.answer("Only owner of the chat can cancel this operation.")
             return
        await event.client.edit_message(event.chat_id, event.query.msg_id, f"Removing of all unapproved users has been cancelled.")

@telethn.on(events.NewMessage(pattern="^/unapproveall"))
async def _(event):
	 chat = await event.get_chat()
	 creator = await c(event)
	 if creator != event.from_id and event.from_id not in SUDO_USERS:
	     await event.reply("Only the chat owner can unapprove all users at once.")
	     return
	 msg = f"Are you sure you would like to unapprove ALL users in {event.chat.title}? This action cannot be undone."
	 await event.client.send_message(event.chat_id, msg, buttons=[[Button.inline('Unapprove all users', b'rmapp')], [Button.inline('Cancel', b'can')]], reply_to=event.id)

@run_async
def unapproveall(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = update.effective_user
    member = chat.get_member(user.id)
    if member.status != "creator" and user.id not in SUDO_USERS:
        update.effective_message.reply_text(
            "Only the chat owner can unapprove all users at once."
        )
    else:
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Unapprove all users", callback_data="unapproveall_user"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Cancel", callback_data="unapproveall_cancel"
                    )
                ],
            ]
        )
        update.effective_message.reply_text(
            f"Are you sure you would like to unapprove ALL users in {chat.title}? This action cannot be undone.",
            reply_markup=buttons,
            parse_mode=ParseMode.MARKDOWN,
        )


@run_async
def unapproveall_btn(update: Update, context: CallbackContext):
    query = update.callback_query
    chat = update.effective_chat
    message = update.effective_message
    member = chat.get_member(query.from_user.id)
    if query.data == "unapproveall_user":
        if member.status == "creator" or query.from_user.id in SUDO_USERS:
            users = []
            approved_users = sql.list_approved(chat.id)
            for i in approved_users:
                users.append(int(i.user_id))
            for user_id in users:
                sql.disapprove(chat.id, user_id)

        if member.status == "administrator":
            query.answer("Only owner of the chat can do this.")

        if member.status == "member":
            query.answer("You need to be admin to do this.")
    elif query.data == "unapproveall_cancel":
        if member.status == "creator" or query.from_user.id in SUDO_USERS:
            message.edit_text("Removing of all approved users has been cancelled.")
            return ""
        if member.status == "administrator":
            query.answer("Only owner of the chat can do this.")
        if member.status == "member":
            query.answer("You need to be admin to do this.")
				

__help__  = """
Sometimes, you might trust a user not to send unwanted content.
Maybe not enough to make them admin, but you might be ok with locks, blacklists, and antiflood not applying to them.

That's what approvals are for - approve of trustworthy users to allow them to send 

*Admin commands:*
- /approval: Check a user's approval status in this chat.

*Admin commands:*
- /approve: Approve of a user. Locks, blacklists, and antiflood won't apply to them anymore.
- /unapprove: Unapprove of a user. They will now be subject to locks, blacklists, and antiflood again.
- /approved: List all approved users.

*Examples:*
- To approve a user 
-> `/approve @user`
- To unapprove a user
-> `/unapprove @user`
"""

APPROVE = DisableAbleCommandHandler("approve", approve, pass_args=True)
DISAPPROVE = DisableAbleCommandHandler("unapprove", disapprove, pass_args=True)
LIST_APPROVED = DisableAbleCommandHandler("approved", approved, pass_args=True)
APPROVAL = DisableAbleCommandHandler("approval", approval, pass_args=True)
UNAPPROVEALL = DisableAbleCommandHandler("unapproveall", unapproveall)
UNAPPROVEALL_BTN = CallbackQueryHandler(unapproveall_btn, pattern=r"unapproveall_.*")
				
dispatcher.add_handler(APPROVE)
dispatcher.add_handler(DISAPPROVE)
dispatcher.add_handler(LIST_APPROVED)
dispatcher.add_handler(APPROVAL)
dispatcher.add_handler(UNAPPROVEALL)
dispatcher.add_handler(UNAPPROVEALL_BTN)


__mod_name__ = "Approval"
__command_list__ = ["approve", "unapprove", "approved", "approval"]
__handlers__ = [APPROVE, DISAPPROVE,LIST_APPROVED, APPROVAL]
