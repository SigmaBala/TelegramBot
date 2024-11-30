from MyTgBot import mongodb

db = mongodb["flood"]

async def is_flood_on(chat_id: int) -> bool:
    chat = db.find_one({"chat_id": chat_id})
    if not chat:
        return True
    return False


async def flood_on(chat_id: int):
    is_flood = is_flood_on(chat_id)
    if is_flood:
        return
    return db.delete_one({"chat_id": chat_id})


async def flood_off(chat_id: int):
    is_flood = is_flood_on(chat_id)
    if not is_flood:
        return
    return db.insert_one({"chat_id": chat_id})
