import json
import re, io
from telegraph import upload_file
from pyrogram import types


async def grap(path):
     try:
         grap = upload_file(path)
         for id in grap:
              url = f"https://graph.org{id}"
     except:
          return False
     return url


async def serialize_inline_keyboard(keyboard):
    serialized_keyboard = {
        "inline_keyboard": []
    }
    for row in keyboard.inline_keyboard:
        serialized_row = []
        for button in row:
            serialized_button = {
                "text": button.text,
                "url": button.url
            }
            serialized_row.append(serialized_button)
        serialized_keyboard["inline_keyboard"].append(serialized_row)
    return serialized_keyboard


async def deserialize_inline_keyboard(serialized_keyboard):
    inline_keyboard = []
    for serialized_row in serialized_keyboard["inline_keyboard"]:
        row = []
        for serialized_button in serialized_row:
            button = types.InlineKeyboardButton(**serialized_button)
            row.append(button)
        inline_keyboard.append(row)
    return types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def get_note_deatils(msg):
     reply = msg.reply_to_message
     text = None
     file_id = None
     caption = None
     type = None
     keyboard = None
     keyboard_class = msg.reply_markup if not reply and msg.reply_markup else reply.reply_markup if reply and reply.reply_markup else None
     if keyboard_class:
          keyboard = json.dumps(serialize_inline_keyboard(keyboard_class))
              
     if msg.text and not reply:
        note_name = msg.text.split()[1].lower()
        text = msg.text.split(None, 2)[2]
        type = "#TEXT"
     elif reply:
           note_name = msg.text.split()[1].lower()
           if reply.text:
               text = reply.text
               type = "#TEXT"
           elif reply.sticker:
               file_id = reply.sticker.file_id
               type = "#STICKER"
           elif reply.photo:
               file_id = reply.photo.file_id
               type = "#PHOTO"
               if reply.caption:
                   caption = reply.caption               
           elif reply.video:
               file_id = reply.video.file_id
               type = "#VIDEO"
               if reply.caption:
                   caption = reply.caption  
           elif reply.animation:
               file_id = reply.animation.file_id
               type = "#ANIMATION"
               if reply.caption:
                   caption = reply.caption 
           elif reply.audio:            
               file_id = reply.audio.file_id
               type = "#AUDIO"
               if reply.caption:
                   caption = reply.caption
           elif reply.document:            
               file_id = reply.document.file_id
               type = "#DOCUMENT"
               if reply.caption:
                   caption = reply.caption
     return {
         'name': note_name,
         'text': text, 
         'file_id': file_id,
         'type': type, 
         'caption': caption,
         'keyboard': keyboard
     }
