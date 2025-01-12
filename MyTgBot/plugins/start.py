from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.types.bots_and_keyboards.inline_keyboard_button import InlineKeyboardButton
from pyrogram.types.bots_and_keyboards.inline_keyboard_markup import InlineKeyboardMarkup
from pyrogram.types import CallbackQuery
from MyTgBot import bot
from MyTgBot.database.user_db import add_user, add_group

START_TEXT = """
Hello there i am Serena ✘

I have lot of useful features and i can easily manage your groups!
"""

buttons = [
        [
            InlineKeyboardButton(
                "➕ Add Me", url="https://t.me/CuteSerenaBot?startgroup=true&admin=manage_chat+change_info+post_messages+edit_messages+delete_messages+invite_users+restrict_members+pin_messages+promote_members+manage_video_chats+anonymous=false"),
            InlineKeyboardButton(
                "🆘 Help", callback_data='help_back'),]]



@bot.on_message(filters.command("start"))
async def start(_, message):
   if message.chat.type == ChatType.PRIVATE:    
    await message.reply_text(START_TEXT,
    reply_markup=InlineKeyboardMarkup(buttons),)
    user_id = message.from_user.id
    add_user(message.from_user.id)
   else:
       pm_msg = "I Already Awake!  ( • ̀ω•́  )"
       await message.reply_text(pm_msg)
       add_group(message.chat.id)

@bot.on_message(filters.command("help"))
async def help(_, message):
   if message.chat.type == ChatType.PRIVATE:
    await message.reply_text(HELP_TEXT,
    reply_markup=InlineKeyboardMarkup(HELP_BUTTON),)
    add_user(message.from_user.id)
   else:
     kb = InlineKeyboardMarkup(
        [
          [
            InlineKeyboardButton(
              "Click me for help", 
              url="https://t.me/CuteSerenaBot?start=help",
            ),
          ],
        ],
      )

   await message.reply_text(pm_text,
   reply_markup=kb,)
   add_group(message.chat.id)
pm_text = "Contact me in PM for help!"

HELP_TEXT = """
Click the button below to know my commands!
"""

HELP_BUTTON = [[
        InlineKeyboardButton('💤 Afk', callback_data='afk_help'),
        InlineKeyboardButton('👮 Admin', callback_data='admin_help'),
        InlineKeyboardButton('👥 UserInfo', callback_data='userinfo_help'),
        ],[
        InlineKeyboardButton('🤗 Fun', callback_data='fun_help'),
        InlineKeyboardButton('👻 Misc', callback_data='misc_help'),
        InlineKeyboardButton('🔍 Tagging', callback_data='tagging_help'),
        ],[
        InlineKeyboardButton('✍ Notes', callback_data='notes_help'),
        InlineKeyboardButton('🧚 Nekos', callback_data='nekos_help'),
        InlineKeyboardButton('❌ Ban-All', callback_data='banall_help'),
        ],[
        InlineKeyboardButton('🎤 Voice', callback_data='voice_help'),
        InlineKeyboardButton('☠ Zombies', callback_data='zombies_help'),
        InlineKeyboardButton('✏ Rename', callback_data='rename_help'),
        ],[
        InlineKeyboardButton('🏡 Home', callback_data='home')]]

@bot.on_callback_query(filters.regex("home"))
async def help(_, query: CallbackQuery):
    await query.message.edit_caption(START_TEXT,
                                    reply_markup=InlineKeyboardMarkup(buttons),)

@bot.on_callback_query(filters.regex("help_back"))
async def help(_, query: CallbackQuery):
    await query.message.edit_caption(HELP_TEXT,
                                    reply_markup=InlineKeyboardMarkup(HELP_BUTTON),)

@bot.on_callback_query(filters.regex("close"))
async def close(_, query: CallbackQuery):
           query = query.message
           await query.delete()

BUTTON = [[InlineKeyboardButton("🔙 Back", callback_data="help_back"),
            InlineKeyboardButton("🗑 Close", callback_data='close'),]]

ADMIN_TEXT = """
Usage of Admin commands:
• /admins - to find group admins.
• /promote - promote a user.
• /demote - demote a user.
• /mute - mute a user.
• /unmute - unmute a user.
• /kick - kick a user.
• /ban - ban a user.
• /unban - unban a user.
• /pin - pin a message.
• /unpin - unpin a message.
• /lock - lock a message or anything.
• /unlock - unlock a message or anything.
• /del - delete a message.
• /setgpic - set group pic.
• /setgtitle - set group title.
• /purge - purge a message.
"""

@bot.on_callback_query(filters.regex("admin_help"))
async def adminhelp(_, query: CallbackQuery):
     await query.message.edit_caption(ADMIN_TEXT,
                                      reply_markup=InlineKeyboardMarkup(BUTTON),)

AFK_TEXT = """
Afk:
• /afk - for tell someone in online that your away from using bot.

Example:
`/afk I'm go to office`
`/afk I'm watching tv`
"""

@bot.on_callback_query(filters.regex("afk_help"))
async def afkhelp(_, query: CallbackQuery):
     await query.message.edit_caption(AFK_TEXT,
                                      reply_markup=InlineKeyboardMarkup(BUTTON),)

VOICE_TEXT = """
Voice:
• /voice - reply to a message with the text you want to convert to voice.
"""

@bot.on_callback_query(filters.regex("voice_help"))
async def voicehelp(_, query: CallbackQuery):
     await query.message.edit_caption(VOICE_TEXT,
                                      reply_markup=InlineKeyboardMarkup(BUTTON),)
        
USERINFO_TEXT = """
User Info:
• /id - userid & chatid.
• /info - user information.
"""

@bot.on_callback_query(filters.regex("userinfo_help"))
async def userinfohelp(_, query: CallbackQuery):
     await query.message.edit_caption(USERINFO_TEXT,
                                      reply_markup=InlineKeyboardMarkup(BUTTON),)
        
MISC_TEXT = """
Extra commands:
• /tm - reply media to get telegraph link.
• /txt - reply text with suitable name and get telegraph text link.
• /tr - reply text to translate the message.
• /git - sent github username to view profile.
• /ud - sent word for search urban dictionary.
• /q - reply message to quotly.
• /calc - to calculate sum.
• /write - to write a message.
"""

@bot.on_callback_query(filters.regex("misc_help"))
async def micshelp(_, query: CallbackQuery):
     await query.message.edit_caption(MISC_TEXT,
                                      reply_markup=InlineKeyboardMarkup(BUTTON),)
        
TAGGING_TEXT = """
Tagging a group members:
• /tagall - tag a group members.
• /stop - stop tagging.
"""

@bot.on_callback_query(filters.regex("tagging_help"))
async def tagginghelp(_, query: CallbackQuery):
     await query.message.edit_caption(TAGGING_TEXT,
                                      reply_markup=InlineKeyboardMarkup(BUTTON),)
        
FUN_TEXT = """
Usage of Fun commands:
• /couples - choose 2 users and send their name as couples in your chat.
• /react - react a message.
• /aq - random sent animequotes.
• /dice - sent a dice.
• /truth - sent a truth message.
• /dare - sent a dare message.
"""

@bot.on_callback_query(filters.regex("fun_help"))
async def funhelp(_, query: CallbackQuery):
     await query.message.edit_caption(FUN_TEXT,
                                      reply_markup=InlineKeyboardMarkup(BUTTON),)

NEKOS_TEXT = """
Usage of Animation Reactions commands:
• /neko - random sent neko anime image.
• /waifu - random sent waifu anime image.
• /baka - random sent baka anime image.
• /bore - random sent bore anime image.
• /laugh - random sent laugh anime image.
• /dance - random sent dance anime image.
• /cuddle - random sent cuddle anime image.
• /cry - random sent cry anime image.
• /sleep - random sent sleep anime image.
• /kill - random sent kill anime image.
"""

@bot.on_callback_query(filters.regex("nekos_help"))
async def nekoshelp(_, query: CallbackQuery):
    await query.message.edit_caption(NEKOS_TEXT,
                                    reply_markup=InlineKeyboardMarkup(BUTTON),)

BANALL_TEXT = """
Usage of Banall commands:
Only work for group owner!
• /banall - ban all members in group.
• /unbanall - unban all members in group.
• /kickall - kick all members in group.
"""

@bot.on_callback_query(filters.regex("banall_help"))
async def banallhelp(_, query: CallbackQuery):
     await query.message.edit_caption(BANALL_TEXT,
                                      reply_markup=InlineKeyboardMarkup(BUTTON),)

NOTES_TEXT = """
Save Notes on your chats:
• /save - reply to any messages with notename.
• /clear - use with notename.
• /notes - get notes in your chat. 
"""

@bot.on_callback_query(filters.regex("notes_help"))
async def noteshelp(_, query: CallbackQuery):
     await query.message.edit_caption(NOTES_TEXT,
                                      reply_markup=InlineKeyboardMarkup(BUTTON),)

RENAME_TEXT = """
Usage of Rename commands:
• /rename - reply file to rename.
"""

@bot.on_callback_query(filters.regex("rename_help"))
async def renamehelp(_, query: CallbackQuery):
     await query.message.edit_caption(RENAME_TEXT,
                                      reply_markup=InlineKeyboardMarkup(BUTTON),)

ZOMBIES_TEXT = """
Usage of Zombies commands:
• /zombies clean - Remove delete account on you chat.
"""

@bot.on_callback_query(filters.regex("zombies_help"))
async def zombieshelp(_, query: CallbackQuery):
     await query.message.edit_caption(ZOMBIES_TEXT,
                                      reply_markup=InlineKeyboardMarkup(BUTTON),)

@bot.on_message(filters.new_chat_members)
async def new_chat(_, message):
    bot_id = (await bot.get_me()).id
    add_group(message.chat.id)
    for member in message.new_chat_members:
        if member.id == bot_id:
            await message.reply(
                "🙋‍♂️ Thanks for adding me !"
            )
