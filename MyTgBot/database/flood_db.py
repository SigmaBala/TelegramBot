from MyTgBot import mongodb

db = mongodb["flood"]

async def is_flood_on(chat_id: int) -> bool:
    chat = await db.find_one({"chat_id": chat_id})
    if not chat:
        return True
    return False


async def flood_on(chat_id: int):
    is_flood = await is_flood_on(chat_id)
    if is_flood:
        return
    return await db.delete_one({"chat_id": chat_id})


async def flood_off(chat_id: int):
    is_flood = await is_flood_on(chat_id)
    if not is_flood:
        return
    return await db.insert_one({"chat_id": chat_id})
