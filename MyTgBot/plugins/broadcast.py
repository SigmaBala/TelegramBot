from pyrogram.types import Message
from pyrogram import filters, errors, enums
from MyTgBot import bot
from pyrogram.errors.exceptions.flood_420 import FloodWait
from MyTgBot.database.user_db import add_user, add_group, all_users, all_groups, users, groups, remove_user
import asyncio

@bot.on_message(filters.command(["stats", "users"], ["/", "!", ".", "?"]))
async def dbtool(_, m : Message):
    if m.from_user.id !=1666544436:
         return await m.reply_text("`You Don't Have Enough Rights To Do This!`")    
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)    
    await m.reply_text(text=f"""
📊 Chats Stats
🙋‍♂️ Users : `{xx}`
👥 Groups : `{x}`
🚧 Total users & groups : `{tot}` """)

@bot.on_message(filters.command(["bcast", "broadcast", "usercast"], ["/", "!", "?", "."]))
async def bcast(_, m : Message):
    if m.from_user.id !=1666544436:
         return await m.reply_text("`You Don't Have Enough Rights To Do This!`")
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            if m.reply_to_message:
                await m.reply_to_message.copy(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅ Successfull to sent `{success}` users.\n❌ Faild to sent `{failed}` users.\n👾 Found `{blocked}` Blocked users. \n👻 Found `{deactivated}` Deactivated users.")

@bot.on_message(filters.command(["gcast", "groupcast"], ["/", "?", "!", "."]))
async def gcast(_, m : Message):
    if m.from_user.id !=1666544436:
         return await m.reply_text("`You Don't Have Enough Rights To Do This!`")
    allgroups = groups
    lel = await m.reply_text("`⚡ Processing...`")
    success = 0
    failed = 0
    for grps in allgroups.find():
        try:
            chatid = grps["chat_id"]
            if m.reply_to_message:
                await m.reply_to_message.copy(int(chatid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅ Successfull to sent `{success}` groups.\n❌ Faild to sent `{failed}` groups.")
