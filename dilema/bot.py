# Press Button
# Copyright (C) 2023 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/Press_Button/ >
# PLease read the GNU v3.0 License Agreement in
# <https://www.github.com/KuuhakuTeam/Press_Button/blob/master/LICENSE/>.
 
 
import os 
 
from pyrogram import Client 
from dotenv import load_dotenv 
 
 
if os.path.isfile("config.env"): 
    load_dotenv("config.env") 
 
 
API_ID = int(os.environ.get("API_ID")) 
API_HASH = os.environ.get("API_HASH") 
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GP_LOGS = int(os.environ.get("GP_LOGS")) # id to logs group
DB_URI = os.environ.get("DB_URI")
OWNER = [  # dev list
        838926101,  # @fnixdev <= put your id here
]

press_button = Client( 
    name="press_button", 
    api_id=API_ID, 
    api_hash=API_HASH,  
    bot_token=BOT_TOKEN,  
    in_memory=True 
) 