from pyrogram import Client
from pymongo import MongoClient
import os
import time

start = time.time()

api_id = os.getenv("API_ID", 8497541)
api_hash = os.getenv("API_HASH", "add27f9775d4530a5ee0b6defc874b1f")
bot_token = os.getenv("TOKEN", "6005606875:AAF7QlHsP0MkbFn5AEYquJuF5R7St7wR44k")


MONGO = "mongodb+srv://kora3244:jNtUZleBWM71f1pC@haremdb.qxtdvdh.mongodb.net/?retryWrites=true&w=majority"
mongo = MongoClient(MONGO)
mongodb = mongo.BOT


bot = Client("MyTgBot", 
       api_id=api_id, 
       api_hash=api_hash,
       bot_token=bot_token,
       plugins=dict(root="MyTgBot"), )
