from MyTgBot import bot
from pyrogram.types import Message, ChatPermissions
from pyrogram import filters

@bot.on_message(filters.command("mute",  ["/", ".", "?", "!"]))
async def muted(_, m):
    if len(m.text.split()) > 1:
      admin = await bot.get_chat_member(m.chat.id, m.from_user.id)
      bot_stats = await bot.get_chat_member(m.chat.id, "self")
      user_id = m.from_user.id
      chat_id = m.chat.id
      reply = m.reply_to_message
      try:
          if admin.privileges.can_restrict_members:
                if not reply and len(m.command) >2:
                    mute_id = int(m.text.split()[1])
                    reason = m.text.split(None, 2)[2]
                elif not reply and len(m.command) == 2:
                    mute_id = int(m.text.split()[1])
                    reason = "No Reason Provide"
                elif reply and len(m.command) >1:
                    mute_id = reply.from_user.id
                    reason = m.text.split(None, 1)[1]        
                elif reply and len(m.command) <2:
                     mute_id = reply.from_user.id
                     reason = "No Reason Provide"
                else:
                    return await m.reply("**You are missing the admin rights `can_restrict_members`**")
                if not bot_stats.privileges:
                      return await m.reply_text("`Make you sure I'm Admin!`")
                else:
                     await bot.restrict_chat_member(chat_id, mute_id, ChatPermissions(can_send_messages=False))
                     await m.reply_text(f"The Bitch Muted!\n • {reply.from_user.mention}\n\nFollowing Reason:\n`{reason}`")
      except Exception as e:
             await m.reply_text(e)


@bot.on_message(filters.command("unmute",  ["/", ".", "?", "!"]))
async def unmute(_, m):
    if len(m.text.split()) > 1:
      chat_id = m.chat.id
      user_id = m.from_user.id
      admin = await bot.get_chat_member(m.chat.id, m.from_user.id)
      try:
          if not admin.privileges.can_restrict_members:
                return await m.reply_text("**You are missing the admin rights `can_restrict_members`**")
          else:
             await bot.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True))
             await m.reply_text(f"`Fine they can speck now!`")
      except Exception as e:
            await m.reply_text(e)
