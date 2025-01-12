import random

from MyTgBot import bot, prefix 
from MyTgBot.game.main import ask_to_dm_first
from MyTgBot.database.main import get_users_list
from MyTgBot.database.bucks import add_bucks_to_db, get_bucks_from_users
from MyTgBot.database.count_won_lose import add_won_count, add_lose_count, get_bet_count
from MyTgBot.database.level import add_level_to_db, get_users_level, level_system
from pyrogram import filters


won_users = []

async def winners_bucks(user_id: int, bucks_spend: int):
      count = won_users.count(user_id)
      bucks = bucks_spend*int(count)+2
      return bucks

@bot.on_message(filters.command("bet", prefix))
async def bet(_, message): 
    user_id = message.from_user.id
    if user_id not in (await get_users_list()):
          return await ask_to_dm_first(message)
    bet_count = await get_bet_count(user_id)
    kk = await level_system(bet_count)
    mm = await get_users_level(user_id)
    if mm != kk:
         await add_level_to_db(user_id, level=kk)
         await message.reply_text(f"⬆️ You Have Reached Level {kk}.")
    try:
          bucks_spend = int(message.text.split(None,1)[1])
    except:
          return await message.reply_text("🆘 Example: /bet 100", quote=True)
    if message.text.split(None,1)[1][0] == "-":
        return await message.reply_text("No!", quote=True)
    bucks_balance = await get_bucks_from_users(user_id)
    if bucks_balance > bucks_spend or bucks_balance == bucks_spend:
        mm = ["lose","won","lose","pro","lose"]
        key = random.choice(mm)
        if key.casefold() == "lose":
              await add_lose_count(user_id=user_id, lose_count=+1)
              await add_bucks_to_db(user_id, -bucks_spend)
              bucks = await get_bucks_from_users(user_id)
              await message.reply_text(f"🚫 You Lose {bucks_spend}. Your Current Bucks Balance `{bucks}`.")
              x = [m for m in won_users if m!= user_id]
              won_users.clear()
              cc = won_users + x
              return 
        elif key.casefold() == "pro":
               won_bucks = bucks_spend*10
               await add_bucks_to_db(user_id=user_id, bucks=won_bucks)
               bucks = await get_bucks_from_users(user_id)
               return await message.reply_text(f"🎊 Pro Bet UwU 🎊. 🎊 You Won {won_bucks}, ✨ Your Current Bucks Balance `{bucks}`.", quote=True)
        elif key.casefold() == "won":
              await add_won_count(user_id=user_id, won_count=+1)
              won_users.append(user_id)
              won_bucks = await winners_bucks(user_id=user_id, bucks_spend=bucks_spend)
              await add_bucks_to_db(user_id=user_id, bucks=won_bucks)
              bucks = await get_bucks_from_users(user_id)
              count = won_users.count(user_id)
              return await message.reply_text(f"🎊 You Won [`{count}`x]: {won_bucks}, ✨ Your Current Balance Bucks {bucks}.", quote=True)
    else:
        return await message.reply_text("You Don't Have This Much Bucks, Check Current Bucks Balance by Tap /profile.")
