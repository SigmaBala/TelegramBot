import os
import re
import asyncio
import time
from pyrogram import *
from pyrogram.types import *
from MyTgBot import bot

Clone = Client("MyTgBot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)

# © By Itz-Zaid Your motherfucker if uh Don't gives credits.
@bot.on_message(filters.private & filters.command("clone"))
async def clone(_, message):
    chat = msg.chat
    text = await msg.reply("Usage:\n\n /clone token")
    cmd = msg.command
    phone = msg.command[1]
    try:
        await text.edit("Booting Your Client")
                   # change this Directry according to ur repo
        bot = Client(":memory:", api_id, api_hash, bot_token, plugins={"root": "MyTgBot"})
        await bot.start()
        idle()
        user = await bot.get_me()
        await msg.reply(f"Your Client Has Been Successfully Started As @{user.username}! ✅ \n\nThanks for Cloning.")
    except Exception as e:
        await msg.reply(f"**ERROR:** `{str(e)}`\nPress /start to Start again.")
#End
##This code fit with every pyrogram Codes just import then @Client Xyz!
