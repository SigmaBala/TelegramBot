from MyTgBot import bot
from MyTgBot import mongodb
coupledb = mongodb["coupledb"]


async def get_chats():
    chats = []
    for x in coupledb.find():
         chats.append(x["_id"])
    return chats
    

async def get_couple(chat_id: int):
    couples = coupledb.find_one({"_id": chat_id})
    if couples:
         men = (await bot.get_users(couples["men"])).mention
         women = (await bot.get_users(couples["women"])).mention
         text = f"""
** ♥️ Couples of this Day ❤️**

**Man**: {men}
**Woman**: {women}
"""
         return text

async def save_couple(chat_id: int, date, men, women):
      COUPLES = {"_id":chat_id,"date":date,"men":men,"women":women}
      coupledb.insert_one(COUPLES)



async def check_couple(chat_id: int, date, men, women):
     couples = coupledb.find_one({"_id": chat_id})
     if couples["date"] == date:
         return await get_couple(chat_id)
     else:
         coupledb.update_one({"_id":chat_id},{"$set":{"date": date, "men":men, "women":women}})
         return await get_couple(chat_id)
