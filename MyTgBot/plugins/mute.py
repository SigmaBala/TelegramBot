import requests
import random
from MyTgBot import bot
from pyrogram.types import *
from pyrogram import filters

@bot.on_message(filters.command("mute"))
async def muted(_, message):
      admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
      bot_stats = await bot.get_chat_member(chat.id, "self")
      user_id = int(message.from_user.id)
      chat_id = int(message.chat.id)
      reply = message.reply_to_message
      api = requests.get("https://nekos.best/api/v2/bored").json()
      url = api["results"][0]['url']
      try:
          if admin.privileges.can_restrict_members:   
                if not reply and len(message.command) >2:
                    mute_id = int(message.text.split(" ")[1])
                    reason = message.text.split(None, 2)[2]
                elif not reply and len(message.command) == 2:
                    mute_id = int(message.text.split(" ")[1])
                    reason = "No Reason Provide"
                elif reply and len(message.command) >1:
                    mute_id = reply.from_user.id
                    reason = message.text.split(None, 1)[1]        
                elif reply and len(message.command) <2:
                     mute_id = reply.from_user.id
                     reason = "No Reason Provide"
                else:
                    return await message.reply("I can't find the user.")
                if not bot_stats.privileges:
                      return await message.reply_text("`Make you sure I'm Admin!`")
                if admin.privileges:
                       return await message.reply_text("`The User Is Admin! I can't ban!`")
                else:
                     await bot.restrict_chat_member(chat_id, mute_id, ChatPermissions(can_send_messages=False))
                     await message.reply_animation(url,caption=f"The Bitch Muted!\n • `{mute_id}`\n\nFollowing Reason:\n`{reason}`",
                     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Unmute", callback_data=f"unmute_btn:{mute_id}")]]))
      except Exception as e:
         await message.reply_text(e)
                     


@bot.on_callback_query(filters.regex("unmute_btn"))
async def unmute_btn(_, query):
      chat_id = query.message.chat.id
      user_id = query.from_user.id
      admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
      mute_id = query.data.split(":")[1]
      api = requests.get("https://nekos.best/api/v2/smile").json()
      url = api["results"][0]['url']
      try:
          if not admin.privileges:
                return await query.answer("Admins Only!")
          else:
             await bot.restrict_chat_member(chat_id, mute_id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True))
             await query.message.edit_media(media=InputMediaAnimation(url,caption=f"`fine they can speck now!`\nID: `{mute_id}`"))
      except Exception as e:
            await query.message.reply_text(e)
