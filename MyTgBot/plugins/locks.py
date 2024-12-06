from MyTgBot import bot
from MyTgBot.help.help_func import get_urls_from_text
from pyrogram import filters
from pyrogram.errors.exceptions.bad_request_400 import ChatNotModified
from pyrogram.types import ChatPermissions


incorrect_parameters = "Incorrect Parameters, Check Locks Section In Help."
# Using disable_preview as a switch for url checker
# That way we won't need an additional db to check
# If url lock is enabled/disabled for a chat
data = {
    "messages": "can_send_messages",
    "stickers": "can_send_other_messages",
    "gifs": "can_send_other_messages",
    "media": "can_send_media_messages",
    "games": "can_send_other_messages",
    "inline": "can_send_other_messages",
    "url": "can_add_web_page_previews",
    "polls": "can_send_polls",
    "group_info": "can_change_info",
    "useradd": "can_invite_users",
    "pin": "can_pin_messages",
}


async def current_chat_permissions(chat_id):
    perms = []
    perm = (await bot.get_chat(chat_id)).permissions
    if perm.can_send_messages:
        perms.append("can_send_messages")
    if perm.can_send_media_messages:
        perms.append("can_send_media_messages")
    if perm.can_send_other_messages:
        perms.append("can_send_other_messages")
    if perm.can_add_web_page_previews:
        perms.append("can_add_web_page_previews")
    if perm.can_send_polls:
        perms.append("can_send_polls")
    if perm.can_change_info:
        perms.append("can_change_info")
    if perm.can_invite_users:
        perms.append("can_invite_users")
    if perm.can_pin_messages:
        perms.append("can_pin_messages")

    return perms


async def tg_lock(message, permissions: list, perm: str, lock: bool):
    if lock:
        if perm not in permissions:
            return await message.reply_text("Already locked.")
        permissions.remove(perm)
    else:
        if perm in permissions:
            return await message.reply_text("Already Unlocked.")
        permissions.append(perm)

    permissions = {perm: True for perm in list(set(permissions))}

    try:
        await bot.set_chat_permissions(
            message.chat.id, ChatPermissions(**permissions)
        )
    except ChatNotModified:
        return await message.reply_text(
            "To unlock this, you have to unlock 'messages' first."
        )

    await message.reply_text(("Locked." if lock else "Unlocked."))


@bot.on_message(filters.command(["lock", "unlock"]))
async def locks_func(_, message):
    if len(message.command) != 2:
        return await message.reply_text(incorrect_parameters)

    chat_id = message.chat.id
    parameter = message.text.strip().split(None, 1)[1].lower()
    state = message.command[0].lower()
    admin = await bot.get_chat_member(message.chat.id, message.from_user.id)

    if not admin.privileges.can_restrict_members:
          return await message.reply_text("**You are missing the admin rights `can_restrict_members`**")

    if parameter not in data and parameter != "all":
        return await message.reply_text(incorrect_parameters)

    permissions = await current_chat_permissions(chat_id)

    if parameter in data:
        await tg_lock(
            message,
            permissions,
            data[parameter],
            bool(state == "lock"),
        )
    elif parameter == "all" and state == "lock":
        await bot.set_chat_permissions(chat_id, ChatPermissions())
        await message.reply_text(f"Locked Everything in {message.chat.title}")

    elif parameter == "all" and state == "unlock":
        await bot.set_chat_permissions(
            chat_id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_send_polls=True,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=False,
            ),
        )
        await message.reply(f"Unlocked Everything in {message.chat.title}")


@bot.on_message(filters.command("locks") & ~filters.private)
async def locktypes(_, message):
    permissions = await current_chat_permissions(message.chat.id)

    if not permissions:
        return await message.reply_text("No Permissions.")

    perms = ""
    for i in permissions:
        perms += f"__**{i}**__\n"

    await message.reply_text(perms)


@bot.on_message(filters.text & ~filters.private, group=69)
async def url_detector(_, message):
    user = message.from_user
    chat_id = message.chat.id
    text = message.text.lower().strip()

    if not text or not user:
        return

    check = get_urls_from_text(text)
    if check:
        permissions = await current_chat_permissions(chat_id)
        if "can_add_web_page_previews" not in permissions:
            try:
                await message.delete()
            except Exception:
                await message.reply_text(
                    "This message contains a URL, "
                    + "but i don't have enough permissions to delete it"
            )
