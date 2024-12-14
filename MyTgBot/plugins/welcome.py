from pyrogram import filters
from MyTgBot import bot

@bot.on_message(filters.new_chat_members)
async def welcome(_, m):
        await m.reply("Hello dear {}\nWelcome to **{}**!".format(m.from_user.mention,m.chat.title))
        
@bot.on_message(filters.left_chat_member)
async def member_has_left(_, m):
        await m.reply("Sad to see you leaving **{}**\nTake Care!".format(m.from_user.mention))
