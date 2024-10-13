from pyrogram import filters, enums
from MyTgBot import bot

@bot.on_message(filters.command("zombiesclean"))
async def ban_deleted_accounts(_, m):
    get = await bot.get_chat_member(m.chat.id, m.from_user.id)
    reply = m.reply_to_message
    chat_id = m.chat.id
    deleted_users = []
    banned_users = 0
    if not get.privileges:
         return await m.reply("**You Needs Admin Rights to Control Me (~_^)!**")
    if not get.privileges.can_restrict_members:
         return await m.reply_text(text = "**Your missing the admin rights `can_restrict_members`**")
    m = await m.reply("Finding ghosts...")

    async for i in bot.get_chat_members(chat_id):
        if i.user.is_deleted:
            deleted_users.append(i.user.id)
    if len(deleted_users) > 0:
        for deleted_user in deleted_users:
            try:
                await m.chat.ban_member(deleted_user)
            except Exception:
                pass
            banned_users += 1
        await m.edit(f"Banned {banned_users} Deleted Accounts")
    else:
        await m.edit("There are no deleted accounts in this chat")
