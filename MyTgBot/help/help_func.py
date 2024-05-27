import json
from telegraph import upload_file
from MyTgBot import aiohttpsession
from pyrogram import types

async def grap(path):
     try:
         grap = upload_file(path)
         for id in grap:
              url = f"https://graph.org{id}"
     except:
          return False
     return url

async def get(url: str, *args, **kwargs):
    async with aiohttpsession.get(url, *args, **kwargs) as resp:
        try:
            data = await resp.json()
        except Exception:
            data = await resp.text()
    return data
