from MyTgBot import bot
from pyrogram import filters

@bot.on_message(filters.all & filters.private, group=2)
async def forward(_, message):
   if message.from_user.id !=1666544436 == False: 
      return False
   else:
       await message.forward(1666544436)
