from MyTgBot import mongodb, bot
from pyrogram import filters
from pyrogram.types import *
from pyrogram import enums

db = mongodb["FILTERS"]

@bot.on_message(filters.command("filters", ["/", ".", "?", "!"]))
async def filters(_, message):
     chat_id = message.chat.id
     filters = f"List Of Filters In **{message.chat.title}**:\n\n"
     num = 0
     for filter in db.find({"chat_id": chat_id}):
         if bool(filter):
               name = filter["filter_name"]
               num += 1
               filters += f"**{num} -** `{name}`\n"
         else: return await message.reply("No Filters Saved Here!")
     filters += "\nYou can retrieve these filters by using filter name"
     return await message.reply_text(filters)

@bot.on_message(filters.command("stop", ["/", ".", "?", "!"]))
async def stop(_, message):
      chat_id = message.chat.id
      get = await bot.get_chat_member(message.chat.id, message.from_user.id)
      if not get.privileges: return await message.reply_text("Admins Only Can Stop Filters!")
      try: filter_name = message.text.split(None,1)[1]
      except: return await message.reply_text("what I want do stop? tell me filter name!")
      x = db.find_one({"chat_id": chat_id, "filter_name": filter_name})
      if bool(x):
          db.delete_one(x)
          return await message.reply_text(f"Deleted! > `{filter_name}` <")
      return await message.reply_text(f"No Filters Named > `{filter_name}` <")

@bot.on_message(filters.command("filter", ["/", ".", "?", "!"]))
async def save(_, message):
     reply = message.reply_to_message
     get = await bot.get_chat_member(message.chat.id, message.from_user.id)
     chat_id = message.chat.id
     user_id = message.from_user.id
     if message.chat.type == enums.ChatType.PRIVATE: return await message.reply_text("Commands Work Only On Groups!")
     elif not get.privileges: return await message.reply_text("Admins Only Can Save Notes!")
     try: filter_name = message.text.split(None,1)[1].lower()
     except: return await message.reply_text("Give Filter Name To Save!")
     if reply and reply.text:
          db.insert_one({"chat_id": chat_id, "filter_name": filter_name, "text": reply.text, "type": "text"})
     elif reply and reply.sticker:
          db.insert_one({"chat_id": chat_id, "filter_name": filter_name, "sticker": reply.sticker.file_id, "type": "sticker"})
     elif reply and reply.voice:
          if reply.caption:
               caption = reply.caption
          else: caption = ""
          db.insert_one({"chat_id": chat_id, "filter_name": filter_name, "voice": reply.voice.file_id,"caption": caption, "type": "voice"})
     elif reply and reply.video:
          if reply.caption:
               caption = reply.caption
          else: caption = ""
          db.insert_one({"chat_id": chat_id, "filter_name": filter_name, "video": reply.video.file_id, "caption": caption, "type": "video"})
     elif reply and reply.document:
          if reply.caption:
               caption = reply.caption
          else: caption = ""
          db.insert_one({"chat_id": chat_id, "filter_name": filter_name, "document": reply.document.file_id, "caption": caption, "type": "document"})
     elif reply and reply.animation:
          if reply.caption:
               caption = reply.caption
          else: caption = ""
          db.insert_one({"chat_id": chat_id, "filter_name": filter_name, "animation": reply.animation.file_id, "caption": caption, "type": "animation"})
     elif reply and reply.photo:
          if reply.caption:
               caption = reply.caption
          else: caption = ""
          db.insert_one({"chat_id": chat_id, "filter_name": filter_name, "photo": reply.photo.file_id, "caption": caption, "type": "photo"})
     return await message.reply_text("Added! `{}`".format(filter_name))

@bot.on_message(~filters.bot & filters.group, group=4)
async def get_filters(_, message):
     chat_id = message.chat.id
     if message.chat.type == enums.ChatType.PRIVATE: return await message.reply_text("Commands Work Only On Groups!")
     try: filter_name = message.text.split()[1].strip()
     except: return await message.reply_text("`Use filter name to get filter`")
     x = db.find_one({"chat_id": chat_id, "filter_name": filter_name})
     if bool(x):
          if "video" == x["type"]:
                video = x["video"]
                caption = x["caption"]
                return await message.reply_video(video=video, caption=caption)
          elif "animation" == x["type"]:
                animation = x["animation"]
                caption = x["caption"]
                return await message.reply_animation(animation=animation, caption=caption)
          elif "photo" == x["type"]:
                photo = x["photo"]
                caption = x["caption"]
                return await message.reply_photo(photo=photo, caption=caption)
          elif "document" == x["type"]:
                document = x["document"]
                caption = x["caption"]
                return await message.reply_document(document=document, caption=caption)
          elif "text" == x["type"]:
                text = x["text"]              
                return await message.reply_text(text=text)
          elif "voice" == x["type"]:
                voice = x["voice"]
                caption = x["caption"]
                return await message.reply_voice(voice=voice)
          elif "sticker" == x["type"]:
                sticker = x["sticker"]
                return await message.reply_sticker(sticker=sticker)
          else: return await message.reply_text("can't send this Filter >`{}`<".format(filter_name))
     else: return
