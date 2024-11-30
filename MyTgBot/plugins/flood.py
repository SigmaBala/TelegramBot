from asyncio import get_running_loop, sleep
from datetime import datetime, timedelta

from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    ChatPermissions,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from MyTgBot import bot, mongodb
from MyTgBot.database import flood_off, flood_on, is_flood_on


DB = mongodb["flood"]  # TODO Use mongodb instead of a fucking dict.


def reset_flood(chat_id, user_id=0):
    for user in DB[chat_id].keys():
        if user != user_id:
            DB[chat_id][user] = 0


async def flood_control_func(_, message: Message):
    if not message.chat:
        return
    chat_id = message.chat.id
    if not (await is_flood_on(chat_id)):
        return
    # Initialize db if not already.
    if chat_id not in DB:
        DB[chat_id] = {}

    if not message.from_user:
        reset_flood(chat_id)
        return

    user_id = message.from_user.id
    mention = message.from_user.mention

    if user_id not in DB[chat_id]:
        DB[chat_id][user_id] = 0

    # Reset flood db of current chat if some other user sends a message
    reset_flood(chat_id, user_id)

    # Mute if user sends more than 10 messages in a row
    if DB[chat_id][user_id] >= 10:
        DB[chat_id][user_id] = 0
        try:
            await message.chat.restrict_member(
                user_id,
                permissions=ChatPermissions(),
                until_date=datetime.now() + timedelta(minutes=60),
            )
        except Exception:
            return
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="🚨  Unmute  🚨",
                        callback_data=f"unmute_{user_id}",
                    )
                ]
            ]
        )
        m = await message.reply_text(
            f"Imagine flooding the chat in front of me, Muted {mention} for an hour!",
            reply_markup=keyboard,
        )

        async def delete():
            await sleep(3600)
            try:
                await m.delete()
            except Exception:
                pass

        loop = get_running_loop()
        return loop.create_task(delete())
    DB[chat_id][user_id] += 1


@bot.on_callback_query(filters.regex("unmute_"))
async def flood_callback_func(_, cq: CallbackQuery):
    from_user = cq.from_user
    permissions = await bot.get_chat_member(cq.message.chat.id, from_user.id)
    if permissions.privileges.can_restrict_members:
        return await cq.answer(
            "You don't have enough permissions to perform this action.\n",
            show_alert=True
        )
    user_id = cq.data.split("_")[1]
    await cq.message.chat.unban_member(user_id)
    text = cq.message.text.markdown
    text = f"~~{text}~~\n\n"
    text += f"__User unmuted by {from_user.mention}__"
    await cq.message.edit(text)


@bot.on_message(filters.command("flood"))
async def flood_toggle(_, message: Message):
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if admin.privileges.can_change_info:
       return await message.reply_text("You don't have enough permissions to perform this action.")
    if len(message.command) != 2:
        return await message.reply_text("Usage: /flood [ENABLE|DISABLE]")
    if status == "enable":
        await flood_on(chat_id)
        await message.reply_text("Enabled Flood Checker.")
    elif status == "disable":
        await flood_off(chat_id)
        await message.reply_text("Disabled Flood Checker.")
    else:
        await message.reply_text("Unknown Suffix, Use /flood [ENABLE|DISABLE]")
