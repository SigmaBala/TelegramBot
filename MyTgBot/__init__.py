from pyrogram import Client
from pymongo import MongoClient
import os
import time, logging

start = time.time()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("TOKEN")

log = logging.getLogger(__name__)


# enable logging
FORMAT = "[Telegram-bot] %(message)s"
logging.basicConfig(
    level=logging.INFO, format=FORMAT
)


MONGO = "mongodb+srv://kora3244:jNtUZleBWM71f1pC@haremdb.qxtdvdh.mongodb.net/?retryWrites=true&w=majority"
mongo = MongoClient(MONGO)
mongodb = mongo.BOT


bot = Client("MyTgBot", 
       api_id=api_id, 
       api_hash=api_hash,
       bot_token=bot_token,
       plugins=dict(root="MyTgBot"), )
