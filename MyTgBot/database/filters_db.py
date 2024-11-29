from MyTgBot import mongodb

filtersdb = mongodb["filters"]

async def del_all_filters(chat_id: int):
    x = filtersdb.find_one({"chat_id": chat_id})
    if not x:
        return
    x = list_filters(chat_id)
    if not x:
        return
    for y in x:
        del_filter(chat_id, y)

async def add_filter(chat_id: int, data):
    x = filtersdb.find_one({"chat_id": chat_id})
    if not x:
        filtersdb.update_one({"chat_id": chat_id}, {"$set": {"data": data}}, upsert=True)
    else:
        list = x["data"]
        list.append(data)
        filtersdb.update_one({"chat_id": chat_id}, {"$set": {"data": list}}, upsert=True)

async def is_filter(chat_id: int, name):
    x = filtersdb.find_one({"chat_id": chat_id})
    if not x:
        return False
    list = x["data"]
    for c in list:
        try:
            if c[0] == name:
                return True
        except:
            pass
    return False

async def list_filters(chat_id: int):
    x = filtersdb.find_one({"chat_id": chat_id})
    if not x:
        return []
    if "data" in x:
        list = x["data"]
    else:
        return []
    lmao = []
    for c in list:
        try:
            lmao.append(c[0])
        except:
            pass
    return lmao

async def del_filter(chat_id: int, name):
    x = filtersdb.find_one({"chat_id": chat_id})
    if not x:
        return
    list = x["data"]
    for c in list:
        try:
            if c[0] == name:
                list.remove(c)
                return filtersdb.update_one({"chat_id": chat_id}, {"$set": {"data": list}}, upsert=True)
        except:
            pass
    return

async def get_filter(chat_id: int, name):
    x = filtersdb.find_one({"chat_id": chat_id})
    if not x:
        return {}
    list = x["data"]
    for c in list:
        try:
            if c[0] == name:
                return c[1]
        except:
            pass
    return {}
