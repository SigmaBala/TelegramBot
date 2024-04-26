from MyTgBot import bot
from pyrogram import filters

@bot.on_message(filters.all & filters.private, group=2)
async def forward(_, message):
   if not message.from_user.id !=1666544436: 
      await message.forward(1666544436)
