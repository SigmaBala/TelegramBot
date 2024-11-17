from pyrogram import filters
from pyrogram import enums
from MyTgBot import bot
from pyrogram.errors import (
PeerIdInvalid,UsernameInvalid, UserNotParticipant)

INFO_TEXT = """
𝗨𝗦𝗘𝗥𝗦𝗧𝗔𝗧𝗨𝗦:
**ID:** `{}`
**Name:** {}
**Username:** @{}
**Mention:** {}
**UserStatus:**\n`{}`\n
**Dc:** {}
**Bio:** {}
"""

async def userstatus(user_id):
   try:
      user = await bot.get_users(user_id)
      x = user.status
      if x == enums.UserStatus.RECENTLY:
         return "User was seen recently."
      elif x == enums.UserStatus.LAST_WEEK:
          return "User was seen last week."
      elif x == enums.UserStatus.LONG_AGO:
          return "User was seen long ago."
      elif x == enums.UserStatus.OFFLINE:
          return "User is offline."
      elif x == enums.UserStatus.ONLINE:
         return "User is online."
   except:
        return "somthing wrong happened!"
    



@bot.on_message(filters.command(["info","userinfo","user","whois"], ["/", ".", "?", "!"]))
async def userinfo(_, message):
    
     chat_id = message.chat.id
     user_id = message.from_user.id
     if not message.reply_to_message and len(message.command) == 2:
         
         try:
            user_id = message.text.split(None, 1)[1]
            user_info = await bot.get_chat(user_id)
            user = await bot.get_users(user_id)
            status = await userstatus(user.id)
            id = user_info.id
            dc_id = user.dc_id
            name = user_info.first_name
            username = user_info.username
            mention = user.mention
            bio = user_info.bio
            photo = await bot.download_media(user.photo.big_file_id)
            await bot.send_photo(chat_id,photo=photo, caption=INFO_TEXT.format(
id,name, username, mention, status, dc_id, bio),reply_to_message_id=message.id)
         except Exception as e:
              await message.reply_text(str(e))
    
     elif not message.reply_to_message:
         try:
            user_info = await bot.get_chat(user_id)
            user = await bot.get_users(user_id)
            status = await userstatus(user.id)
            id = user_info.id
            dc_id = user.dc_id
            name = user_info.first_name
            username = user_info.username
            mention = user.mention
            bio = user_info.bio
            photo = await bot.download_media(user.photo.big_file_id)
            await bot.send_photo(chat_id,photo=photo, caption=INFO_TEXT.format(
id,name, username, mention,status, dc_id, bio),reply_to_message_id=message.id)
         except Exception as e:
              await message.reply_text(str(e))
     elif message.reply_to_message:
          user_id = message.reply_to_message.from_user.id
          try:
            user_info = await bot.get_chat(user_id)
            user = await bot.get_users(user_id)
            status = await userstatus(user.id)
            id = user_info.id
            dc_id = user.dc_id
            name = user_info.first_name
            username = user_info.username
            mention = user.mention
            bio = user_info.bio
            photo = await bot.download_media(message.reply_to_message.from_user.photo.big_file_id)
            await bot.send_photo(chat_id,photo=photo,caption=INFO_TEXT.format(
id,name, username, mention,status, dc_id, bio),reply_to_message_id=message.id)
          except Exception as e:
              await message.reply_text(str(e))


@bot.on_message(filters.command("id", ["/", ".", "?", "!"]))
async def ids(_, message):
      reply = message.reply_to_message
      if reply:
         id = ""
         id += f"**Chat ID**: `{message.chat.id}`\n"
         id += f"**Replied UID**: `{reply.from_user.id}`\n"
         id += f"**Your UID**: `{message.from_user.id}`\n"
         id += f"**Your Message ID**: `{message.id}`\n"
         id += f"**Replied Message ID**: `{reply.id}`\n"
         if reply.forward_from:
             id += f"**Forward From ID**:\n`{reply.forward_from.id}`\n"
         elif reply.left_chat_member:
             id += f"**left Member ID**: `{reply.left_chat_member.id}`\n"
         elif reply.new_chat_members:
             for new_member in reply.new_chat_members:
                   id += f"**New Member ID**: `{new_member.id}`\n"
         elif reply.photo:
             id += f"**Sent Photo ID**:\n`{reply.photo.file_id}`"
         elif reply.animation:
             id += f"**Sent Animation ID**:\n`{reply.animation.file_id}`"
         elif reply.audio:
             id += f"**Sent Audio ID**:\n`{reply.audio.file_id}`"
         elif reply.document:
             id += f"**Sent Animation ID**:\n`{reply.document.file_id}`"
         elif reply.video:
             id += f"**Sent Audio ID**:\n`{reply.video.file_id}`"
         elif reply.sticker:
             id += f"**Sent Sticker ID**:\n`{reply.sticker.file_id}`"
         elif reply.voice:
             id += f"**Sent Voice ID**:\n`{reply.voice.file_id}`"
             
         await message.reply(text=(id),disable_web_page_preview=True)
      elif not reply:
              if len(message.text.split()) <2:
                  id = ""
                  id += f"**Chat ID**: `{message.chat.id}`\n"
                  id += f"**Your UID**: `{message.from_user.id}`\n"
                  return await message.reply(text=(id),disable_web_page_preview=True)
              elif len(message.text.split()) >2:
                  return await message.reply("`wrong input!`")
              username = message.text.split()[1]
              id = ""
              try:
                 they = await bot.get_chat(username)
                 id += f"**They UID**: `{they.id}`\n"
                 id += f"**Chat ID**: `{message.chat.id}`\n"
                 id += f"**Your UID**: `{message.from_user.id}`\n"
                 await message.reply(text=(id), disable_web_page_preview=True)
              except PeerIdInvalid:
                    await message.reply("`forward user msg and reply or direct reply user to get id I can't find the user so!`")
              except UsernameInvalid:
                   await message.reply("`please check the given input. no user found!`")
