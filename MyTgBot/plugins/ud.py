import request
from pyrogram import filters
from MyTgBot import bot

@bot.on_message(filters.command(["ud","define"], ["/", "!", ".", "?"]))
async def ud(_, message):
        if len(message.command) < 2:
             return await message.reply_text("where you input the text?")         
        text = message.text.split(None, 1)[1]
        try:
          results = requests.get(
            f'https://api.urbandictionary.com/v0/define?term={text}').json()
          reply_text = f'**results: {text}**\n\n{results["list"][0]["definition"]}\n\n_{results["list"][0]["example"]}_'
        except Exception as e: 
              return await message.edit_text(f"Somthing wrong Happens:\n`{e}`")
        ud = await message.edit_text("Exploring....")
        await ud.edit_text(reply_text)
