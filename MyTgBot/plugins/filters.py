from pyrogram import filters
from pyrogram.types import *
from MyTgBot import bot
from MyTgBot.database.filters_db import *
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM

markup = IKM(
         [
         [
         IKB("Clear 🗑️", callback_data="clear_filters")
         ]
         ]
         )

@bot.on_callback_query(filters.regex("clear_filters"))
async def cbq(_, q):
       id = q.from_user.id
       admin = await bot.get_chat_member(q.message.chat.id, message.from_user.id)
       if not admin.privileges:
            return await q.answer("Only admin can clear all at once !", show_alert=True)
       await q.answer("clearing...")
       await del_all_filters(q.message.chat.id)
       await q.edit_message_text("All filters cleared !")

@bot.on_message(filters.command("filter"))
async def filter(_, message):
       id = message.from_user.id 
       lol = await bot.get_chat_member(message.chat.id, message.from_user.id)
       if not lol.privileges:
            return await message.reply("**You don't have right to do this !**")
        lol = lol.privileges
        if not lol.can_change_info:
            return await message.reply("**You don't have right to edit filters !**")
    reply = message.reply_to_message
    if not reply:
        txt = message.text.split()
        if len(txt) < 3:
            return await message.reply("**/filter trigger text**")
        trigger = message.text.split()[1]
        content = {"file": None, "text": message.text.split(None, 2)[2]}
    if reply:
        if reply.text:
            if len(message.command) < 2:
                return await message.reply("**Give a word to filter it !**")
            trigger = message.text.split()[1]
            content = {"file": None, "text": reply.text}
        elif reply.media:
            caption = reply.caption if reply.caption else None
            if len(message.command) < 2:
                return await message.reply("**Give a word to filter it !**")
            elif reply.photo:
                content = {"file": ["photo", reply.photo.file_id], "text": caption}
            elif reply.video:
                content = {"file": ["video", reply.video.file_id], "text": caption}
            elif reply.sticker:
                content = {"file": ["sticker", reply.sticker.file_id], "text": caption}
            elif reply.document:
                content = {"file": ["document", reply.document.file_id], "text": caption}
            elif reply.audio:
                content = {"file": ["audio", reply.audio.file_id], "text": caption}
            elif reply.voice:
                content = {"file": ["voice", reply.voice.file_id], "text": caption}
            elif reply.animation:
                content = {"file": ["animation", reply.animation.file_id], "text": caption}
            else:
                return
            trigger = message.text.split()[1]
    await add_filter(message.chat.id, [trigger.lower(), content])
    await message.reply(f"**Filter saved ~** `{trigger}`")

@bot.on_message(filters.command("stop"))
async def stopper(_, message):
       id = message.from_user.id
        x = await bot.get_chat_member(message.chat.id, message.from_user.id)
       if not x.privileges:
            return await message.reply("**You don't have right to do this !**")
        x = x.privileges
        if not x.can_change_info:
            return await message.reply("**You don't have right to edit filters !**")
    if len(m.command) < 2:
        return await message.reply("**Give filter name to stop !**")
    filname = message.text.split()[1].lower()
    x = await is_filter(message.chat.id, filname)
    if not x:
        return await message.reply("**No filter saved with this name !**")
        await del_filter(message.chat.id, filname)
        await message.reply(f"**Filter stopped ~** `{filname}`")

@bot.on_message(filters.command("filters"))
async def filter_getter(_, message):
       id = message.from_user.id
        x = await bot.get_chat_member(message.chat.id, message.from_user.id)
       if not x.privileges:
            return await message.reply("**You don't have right to do this !**")
        x = x.privileges
        if not x.can_change_info:
            return await message.reply("**You don't have right to edit filters !**")
    x = await list_filters(message.chat.id)
    if not x:
        return await message.reply(f"**No filters saved in {message.chat.title}**")
    txt = f"**Filters in {message.chat.title}**"
    txt += "\n\n"
    for g in x:
        txt += f"- `{g}`\n"
    await message.reply(txt, reply_markup=markup)

@bot.on_message(filters.group, group=11)
async def cwf(_, message):
    if message.from_user:
        if message.text or message.caption:
            txt = message.text if message.text else message.caption 
            if txt.split()[0].lower() == "/filter":
                return
            x = await list_filters(message.chat.id)
            for h in txt.split():
                h = h.lower()
                if h.lower() in x:
                    j = await get_filter(message.chat.id, h)
                    if not j["file"]:
                        sext = j["text"]
                        return await message.reply(sext)
                    t = j["file"]
                    if t[0] == "photo":
                        return await message.reply_photo(t[1], caption=j["text"] if "text" in j else None)
                    if t[0] == "video":
                        return await message.reply_video(t[1], caption=j["text"] if "text" in j else None)
                    if t[0] == "audio":
                        return await message.reply_audio(t[1], caption=j["text"] if "text" in j else None)
                    if t[0] == "voice":
                        return await message.reply_voice(t[1], caption=j["text"] if "text" in j else None)
                    if t[0] == "document":
                        return await message.reply_document(t[1], caption=j["text"] if "text" in j else None)
                    if t[0] == "animation":
                        return await message.reply_animation(t[1], caption=j["text"] if "text" in j else None)
                    if t[0] == "sticker":
                        return await message.reply_sticker(t[1])
