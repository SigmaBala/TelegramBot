from MyTgBot import mongodb

afkdb = mongodb["afk"] 


async def is_afk(user_id: int) -> bool:
    user = afkdb.find_one({"user_id": user_id})
    if not user:
        return False, {}
    return True, user["reason"]


async def add_afk(user_id: int, mode):
    afkdb.update_one(
        {"user_id": user_id}, {"$set": {"reason": mode}}, upsert=True
    )


async def remove_afk(user_id: int):
    user = afkdb.find_one({"user_id": user_id})
    if user:
        return afkdb.delete_one({"user_id": user_id})
