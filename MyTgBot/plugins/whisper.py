from pyrogram import filters
from pyrogram.types import InlineQueryResultPhoto, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent
from pyrogram import enums
from MyTgBot import bot


@bot.on_message(filters.command("whisper", ["/", "?", ".", "!"]))
async def startmsg(_, message):
   text = f"""
👋 Hi {message.from_user.mention}

❓ How to use this bot in inline:

`@{bot.me.username} Hi @BARATHXD`
`@{bot.me.username} Hi @all`

"""
   key = InlineKeyboardMarkup (
     [[
       InlineKeyboardButton ("TRY NOW", switch_inline_query='Hi @BARATHXD') ]]
   )
   await message.reply(text, reply_markup=key, quote=True)


@bot.on_inline_query(filters.regex("@"))
async def whisper(_, iquery):
    user = iquery.query.split("@")[1]
    if " " in user: return 
    user_id = iquery.from_user.id
    query = iquery.query.split("@")[0]
    if user == "all":
      text = "🎊 This wisper for all"
      username = "all"
    else:
      try:
       get = await bot.get_chat(user)
       user = get.id
       username = get.username
      except Exception:
        pass
      text = f"**🔒 Secret whisper for ( @{username} ) .ا**"
    reply_markup = InlineKeyboardMarkup(
      [[
        InlineKeyboardButton("📪 Show whisper", callback_data=f"{send.id}catch{user}from{user_id}")
      ]]
    )
    await iquery.answer(
      results=[
       InlineQueryResultArticle(
          title=f"📪 Send whisper for {username}",
          url="http://t.me/NandhaBots",
          input_message_content=InputTextMessageContent(
            message_text=text,
            parse_mode=enums.ParseMode.MARKDOWN 
          ),
          reply_markup=reply_markup
       )
      ],
      cache_time=1
    )

@bot.on_inline_query()
async def whisper(_, query):
    text = f"""
❓ How to use this bot in inline:

@{bot.me.username} Hi @BARATHXD
@{bot.me.username} Hi @all
"""
    await query.answer(
        results=[
            InlineQueryResultPhoto(
                title="🔒 Type the whisper + username",
                photo_url='https://t.me/BARATHXD',
                description=f'@{bot.me.username} Hello @BARATHXD',
                reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ("🔗", url='t.me/NandhaBots')]]),
                input_message_content=InputTextMessageContent(text)
            ),
        ],
        cache_time=1
    )
    
@bot.on_callback_query(filters.regex("catch"))
async def get_whisper(_,query):
    sp = query.data.split("catch")[1]
    user = sp.split("from")[0]
    from_user = int(sp.split("from")[1])
    reply_markup = InlineKeyboardMarkup(
      [
      [
        InlineKeyboardButton("📭 Show whisper", callback_data=query.data)
      ],
      [
        InlineKeyboardButton("🗑️", callback_data=f"DELETE{from_user}")
      ],
      ]
    )
    if user == "all":
       try:
         await query.edit_message_reply_markup(
           reply_markup
         )
       except:
         pass
       return 
    
    else:
      if str(query.from_user.id) == user:
        try:
         await query.edit_message_reply_markup(
           reply_markup
         )
        except:
         pass
        return 
      
      else:
        await query.answer("🔒 This whisper it's not for you .", show_alert=True)
        return 

@bot.on_callback_query(filters.regex("DELETE"))
async def del_whisper(_,query):
   user = int(query.data.split("DELETE")[1])
   if not query.from_user.id == user:
     return await query.answer("❓ Only the sender can use this button .")
   
   else:
     reply_markup = InlineKeyboardMarkup(
      [[
        InlineKeyboardButton("DEV. 🔗", url="https://t.me/BARATHXD")
      ]]
    )
     await query.edit_message_text(f"**🗑️ This whisper was deleted by ( {query.from_user.mention} ) .**",
       reply_markup=reply_markup
     )
