import requests
import random
from MyTgBot import bot
from pyrogram.types import Message, ChatPermissions
from pyrogram import filters

@bot.on_message(filters.command("mute",  ["/", ".", "?", "!"]))
async def muted(_, m):
      admin = await bot.get_chat_member(m.chat.id, m.from_user.id)
      bot_stats = await bot.get_chat_member(m.chat.id, "self")
      user_id = int(m.from_user.id)
      chat_id = int(m.chat.id)
      reply = m.reply_to_message
      try:
          if admin.privileges.can_restrict_members:
                if not reply and len(m.command) >2:
                    mute_id = int(m.text.split(" ")[1])
                    reason = m.text.split(None, 2)[2]
                elif not reply and len(m.command) == 2:
                    mute_id = int(m.text.split(" ")[1])
                    reason = "No Reason Provide"
                elif reply and len(m.command) >1:
                    mute_id = reply.from_user.id
                    reason = m.text.split(None, 1)[1]        
                elif reply and len(m.command) <2:
                     mute_id = reply.from_user.id
                     reason = "No Reason Provide"
                else:
                    return await m.reply("**Your missing the admin rights `can_restrict_members`**")
                if not bot_stats.privileges:
                      return await m.reply_text("`Make you sure I'm Admin!`")
                else:
                     await bot.restrict_chat_member(chat_id, mute_id, ChatPermissions(can_send_messages=False))
                     await m.reply_text(f"The Bitch Muted!\n • {message.from_user.mention}\n\nFollowing Reason:\n`{reason}`")
                     return



