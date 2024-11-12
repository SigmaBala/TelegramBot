import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from MyTgBot import bot
from MyTgBot import api_id, api_hash, bot_token

@bot.on_message(filters.command("clone"))
async def bot_clone(_, msg: Message):
    chat = msg.chat
    cmd = msg.command
    user_id = msg.from_user.id
    try:
        bot_token = msg.text.split()[1]
    except IndexError:
        await msg.reply("Please provide a valid BOT_TOKEN.\nUsage:\n\n /clone BOT_TOKEN.")
        return

    text = await msg.reply("Booting Your Client")
    
    async def start_new_client():
        client_name = f":memory:{user_id}"
        try:
            client = Client(client_name, api_id, api_hash, bot_token, plugins={"root": "MyTgBot"})
            await client.start()
            user = await client.get_me()
            await text.edit(f"Booted Client as @{user.username} Do /start for testing")        
            await msg.reply(f"Your Client Has Been Successfully Started As @{user.username}! ✅ \n\n Use Help For Help Menu\n\nThanks for Cloning.\n **ignore this message its happened due to over load**")
            await pyrogram.idle()
        except Exception as e:
            await msg.reply(f"**ERROR:** `{str(e)}`\nPress /start to Start again.")

    asyncio.create_task(start_new_client())
