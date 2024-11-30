from MyTgBot import bot
from pyrogram import enums


async def is_owner(chat_id: int, user_id: int):
    async for x in bot.get_chat_members(chat_id):
        if x.status == enums.ChatMemberStatus.OWNER:
             if x.user.id == user_id:
                 return True
             else: return False
