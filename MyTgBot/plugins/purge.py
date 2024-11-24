from asyncio import sleep
from pyrogram import filters, enums
from pyrogram.enums import ChatType
from pyrogram.errors import MessageDeleteForbidden, RPCError
from MyTgBot import bot


@bot.on_message(filters.command("purge", ["/", ".", "?", "!"]))
async def purge(_, m):
    reply = m.reply_to_message
    chat = m.chat
    user = m.from_user
    user_stats = await bot.get_chat_member(chat.id, user.id)
    bot_stats = await bot.get_chat_member(chat.id, "self")
    if not bot_stats.privileges:
         return await m.reply_text("Make Me Admin REEE!!")
    if not user_stats.privileges:
         return await m.reply_text("Only Admins are allowed to use this command!")    
    if not reply:
         return  await m.reply_text("reply to message for deleting")
    if not bot_stats.privileges.can_delete_messages:
         return await m.reply_text("**I'm missing the permission of**:\n`can_delete_messages`")
    if not user_stats.privileges.can_delete_messages:
         return await m.reply_text("**you are missing the permission of**:\n`can_delete_messages`")
    if m.chat.type != ChatType.SUPERGROUP:
        await m.reply_text("Cannot Purge Messages Here, Upgrade Your Group To Supergroup")
        return

    if m.reply_to_message:
        message_ids = list(range(m.reply_to_message.id, m.id))

        def divide_chunks(l: list, n: int = 100):
            for i in range(0, len(l), n):
                yield l[i : i + n]

        m_list = list(divide_chunks(message_ids))

        try:
            for plist in m_list:
                await bot.delete_messages(
                    chat_id=m.chat.id,
                    message_ids=plist,
                    revoke=True,
                )
            await m.delete()
        except MessageDeleteForbidden:
            await m.reply_text("Cannot delete all messages. The messages may be too old, I might not have delete rights, or this might not be a supergroup.")
            return
        except RPCError as ef:
            await m.reply_text(f"""Some error occured, Error: {ef}""")

        count_del_msg = len(message_ids)

        z = await m.reply_text(text=f"Deleted **{count_del_msg}** Messages...")
        await sleep(3)
        await z.delete()
        return
    await m.reply_text("Reply to a message to start purge !")
