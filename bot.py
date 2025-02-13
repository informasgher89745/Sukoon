from pyrogram.enums import ChatAction  # Import ChatAction
from pyrogram import Client, filters
from pyrogram.types import *
from pyrogram.enums import ChatMemberStatus  # Correct import
from pymongo import MongoClient
import requests
import random
import os
import re
import asyncio
import time
from datetime import datetime

import config
#from database.users_chats_db import db


API_ID = config.API_ID
API_HASH = config.API_HASH
BOT_TOKEN = config.BOT_TOKEN
MONGO_URL = config.MONGO_URL
BOT_USERNAME = config.BOT_USERNAME
BOT_NAME = config.BOT_NAME


bot = Client(
    "SukoonXbot" ,
    api_id = API_ID,
    api_hash = API_HASH ,
    bot_token = BOT_TOKEN
)

async def is_admins(chat_id: int):
    admins = []
    async for member in bot.get_chat_members(chat_id):
        if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            admins.append(member.user.id)
    return admins


EMOJIOS = [ 
      "❤",
      "💖",
]
      
START = f"""
**๏ Hie Baby❣️ ๏**
"""


from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@bot.on_message(filters.command(["start", "aistart", f"start@{BOT_USERNAME}"]))
async def restart(client, m: Message):
    accha = await m.reply_text(
                text=random.choice(EMOJIOS),
    )
    await asyncio.sleep(1)
    await accha.edit("𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠..")
    await asyncio.sleep(0.1)
    await accha.edit("𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠...")
    await asyncio.sleep(0.1)
    await accha.edit("𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠....")
    await asyncio.sleep(0.1)
    await accha.edit("𝐒𝐭𝐚𝐫𝐭𝐞𝐝.✓")
    await asyncio.sleep(0.2)
    
    # Inline buttons on different lines
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("➕ Add Me", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ],
        [
            InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/AaghaFazal")
        ]
    ])
    
    # Final message with buttons
    await accha.edit(
        f"Hello {m.from_user.first_name}! \nI'm {BOT_NAME}, your friendly chatbot 🤖. \n"
        "I can chat with you, respond to commands, and assist in your groups. \n"
        "Use /chatbot on or /chatbot off to control me in groups. \nEnjoy chatting!",
        reply_markup=buttons 
    )

@bot.on_message(
    filters.command(["chatbot off", f"chatbot@{BOT_USERNAME} off"], prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def chatbotofd(client, message):
    Fazaldb = MongoClient(MONGO_URL)    
    aagha = Fazaldb["SukoonDB"]["Groups"]     
    if message.from_user:
        user = message.from_user.id
        chat_id = message.chat.id
        if user not in await is_admins(chat_id):
           return await message.reply_text(
                "You are not admin"
            )
    is_aagha = aagha.find_one({"chat_id": message.chat.id})
    if not is_aagha:
        aagha.insert_one({"chat_id": message.chat.id})
        await message.reply_text(f"Chatbot Disabled!")
    if is_aagha:
        await message.reply_text(f"ChatBot Already Disabled")
    

@bot.on_message(
    filters.command(["chatbot on", f"chatbot@{BOT_USERNAME} on"] ,prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def chatboton(client, message):
    Fazaldb = MongoClient(MONGO_URL)    
    aagha = Fazaldb["SukoonDB"]["Groups"]     
    if message.from_user:
        user = message.from_user.id
        chat_id = message.chat.id
        if user not in await is_admins(chat_id):

            return await message.reply_text(
                "You are not admin"
            )
    is_aagha = aagha.find_one({"chat_id": message.chat.id})
    if not is_aagha:           
        await message.reply_text(f"Chatbot Already Enabled")
    if is_aagha:
        aagha.delete_one({"chat_id": message.chat.id})
        await message.reply_text(f"ChatBot Enabled!")
    

@bot.on_message(
    filters.command(["chatbot", f"chatbot@{BOT_USERNAME}"], prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def chatbot(client, message):
    await message.reply_text(f"**ᴜsᴀɢᴇ:**\n/**chatbot [on/off]**\n**ᴄʜᴀᴛ-ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅ(s) ᴡᴏʀᴋ ɪɴ ɢʀᴏᴜᴘ ᴏɴʟʏ!**")


@bot.on_message(
 (
        filters.text
        | filters.sticker
    )
    & ~filters.private
    & ~filters.bot,
)
async def aaghaai(client: Client, message: Message):

   chatdb = MongoClient(MONGO_URL)
   chatai = chatdb["Word"]["WordDb"]   

   if not message.reply_to_message:
       Fazaldb = MongoClient(MONGO_URL)
       aagha = Fazaldb["SukoonDB"]["Groups"] 
       is_aagha = aagha.find_one({"chat_id": message.chat.id})
       if not is_aagha:
           await bot.send_chat_action(message.chat.id, ChatAction.TYPING) # ✅ This works fine
           K = []  
           is_chat = chatai.find({"word": message.text})  
           k = chatai.find_one({"word": message.text})      
           if k:               
               for x in is_chat:
                   K.append(x['text'])          
               hey = random.choice(K)
               is_text = chatai.find_one({"text": hey})
               Yo = is_text['check']
               if Yo == "sticker":
                   await message.reply_sticker(f"{hey}")
               if not Yo == "sticker":
                   await message.reply_text(f"{hey}")
   
   if message.reply_to_message:  
       Fazaldb = MongoClient(MONGO_URL)
       aagha = Fazaldb["SukoonDB"]["Groups"] 
       is_aagha = aagha.find_one({"chat_id": message.chat.id})    
       getme = await bot.get_me()
       bot_id = getme.id                             
       if message.reply_to_message.from_user.id == bot_id: 
           if not is_aagha:                   
               await bot.send_chat_action(message.chat.id, ChatAction.TYPING) # ✅ This works fine
               K = []  
               is_chat = chatai.find({"word": message.text})
               k = chatai.find_one({"word": message.text})      
               if k:       
                   for x in is_chat:
                       K.append(x['text'])
                   hey = random.choice(K)
                   is_text = chatai.find_one({"text": hey})
                   Yo = is_text['check']
                   if Yo == "sticker":
                       await message.reply_sticker(f"{hey}")
                   if not Yo == "sticker":
                       await message.reply_text(f"{hey}")
       if not message.reply_to_message.from_user.id == bot_id:          
           if message.sticker:
               is_chat = chatai.find_one({"word": message.reply_to_message.text, "id": message.sticker.file_unique_id})
               if not is_chat:
                   chatai.insert_one({"word": message.reply_to_message.text, "text": message.sticker.file_id, "check": "sticker", "id": message.sticker.file_unique_id})
           if message.text:                 
               is_chat = chatai.find_one({"word": message.reply_to_message.text, "text": message.text})                 
               if not is_chat:
                   chatai.insert_one({"word": message.reply_to_message.text, "text": message.text, "check": "none"})    
               

@bot.on_message(
 (
        filters.sticker
        | filters.text
    )
    & ~filters.private
    & ~filters.bot,
)
async def aaghastickerai(client: Client, message: Message):

   chatdb = MongoClient(MONGO_URL)
   chatai = chatdb["Word"]["WordDb"]   

   if not message.reply_to_message:
       Fazaldb = MongoClient(MONGO_URL)
       aagha = Fazaldb["SukoonDB"]["Groups"] 
       is_aagha = aagha.find_one({"chat_id": message.chat.id})
       if not is_aagha:
           await bot.send_chat_action(message.chat.id, ChatAction.TYPING) # ✅ This works fine
           K = []  
           is_chat = chatai.find({"word": message.sticker.file_unique_id})      
           k = chatai.find_one({"word": message.text})      
           if k:           
               for x in is_chat:
                   K.append(x['text'])
               hey = random.choice(K)
               is_text = chatai.find_one({"text": hey})
               Yo = is_text['check']
               if Yo == "text":
                   await message.reply_text(f"{hey}")
               if not Yo == "text":
                   await message.reply_sticker(f"{hey}")
   
   if message.reply_to_message:
       Fazaldb = MongoClient(MONGO_URL)
       aagha = Fazaldb["SukoonDB"]["Groups"] 
       is_aagha = aagha.find_one({"chat_id": message.chat.id})
       getme = await bot.get_me()
       bot_id = getme.id
       if message.reply_to_message.from_user.id == bot_id: 
           if not is_aagha:                    
               await bot.send_chat_action(message.chat.id, ChatAction.TYPING) # ✅ This works fine
               K = []  
               is_chat = chatai.find({"word": message.text})
               k = chatai.find_one({"word": message.text})      
               if k:           
                   for x in is_chat:
                       K.append(x['text'])
                   hey = random.choice(K)
                   is_text = chatai.find_one({"text": hey})
                   Yo = is_text['check']
                   if Yo == "text":
                       await message.reply_text(f"{hey}")
                   if not Yo == "text":
                       await message.reply_sticker(f"{hey}")
       if not message.reply_to_message.from_user.id == bot_id:          
           if message.text:
               is_chat = chatai.find_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.text})
               if not is_chat:
                   chatai.insert_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.text, "check": "text"})
           if message.sticker:                 
               is_chat = chatai.find_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.sticker.file_id})                 
               if not is_chat:
                   chatai.insert_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.sticker.file_id, "check": "none"})    
               

@bot.on_message(
    (
        filters.text
        | filters.sticker
    )
    & filters.private
    & ~filters.bot,
)
async def aaghaprivate(client: Client, message: Message):

   chatdb = MongoClient(MONGO_URL)
   chatai = chatdb["Word"]["WordDb"]
   if not message.reply_to_message: 
       await bot.send_chat_action(message.chat.id, ChatAction.TYPING) # ✅ This works fine
       K = []  
       is_chat = chatai.find({"word": message.text})                 
       for x in is_chat:
           K.append(x['text'])
       hey = random.choice(K)
       is_text = chatai.find_one({"text": hey})
       Yo = is_text['check']
       if Yo == "sticker":
           await message.reply_sticker(f"{hey}")
       if not Yo == "sticker":
           await message.reply_text(f"{hey}")
   if message.reply_to_message:            
       getme = await bot.get_me()
       bot_id = getme.id       
       if message.reply_to_message.from_user.id == bot_id:                    
           await bot.send_chat_action(message.chat.id, ChatAction.TYPING) # ✅ This works fine
           K = []  
           is_chat = chatai.find({"word": message.text})                 
           for x in is_chat:
               K.append(x['text'])
           hey = random.choice(K)
           is_text = chatai.find_one({"text": hey})
           Yo = is_text['check']
           if Yo == "sticker":
               await message.reply_sticker(f"{hey}")
           if not Yo == "sticker":
               await message.reply_text(f"{hey}")
       

@bot.on_message(
 (
        filters.sticker
        | filters.text
    )
    & filters.private
    & ~filters.bot,
)
async def aaghaprivatesticker(client: Client, message: Message):

   chatdb = MongoClient(MONGO_URL)
   chatai = chatdb["Word"]["WordDb"] 
   if not message.reply_to_message:
       await bot.send_chat_action(message.chat.id, ChatAction.TYPING) # ✅ This works fine
       K = []  
       is_chat = chatai.find({"word": message.sticker.file_unique_id})                 
       for x in is_chat:
           K.append(x['text'])
       hey = random.choice(K)
       is_text = chatai.find_one({"text": hey})
       Yo = is_text['check']
       if Yo == "text":
           await message.reply_text(f"{hey}")
       if not Yo == "text":
           await message.reply_sticker(f"{hey}")
   if message.reply_to_message:            
       getme = await bot.get_me()
       bot_id = getme.id       
       if message.reply_to_message.from_user.id == bot_id:                    
           await bot.send_chat_action(message.chat.id, ChatAction.TYPING) # ✅ This works fine
           K = []  
           is_chat = chatai.find({"word": message.sticker.file_unique_id})                 
           for x in is_chat:
               K.append(x['text'])
           hey = random.choice(K)
           is_text = chatai.find_one({"text": hey})
           Yo = is_text['check']
           if Yo == "text":
               await message.reply_text(f"{hey}")
           if not Yo == "text":
               await message.reply_sticker(f"{hey}")

print(f"The bot has been successfully hosted. \nDeveloped by @AaghaFazal.")      
bot.run()