from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
import random
import os

import openai
from openai import OpenAI
import requests


import asyncio
from telegram import Bot
import re


async def send_message_via_bot(token, chat_id, message):
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=message)


from telegram import Bot


OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Create a Bot instance
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = "-1002274400390"  # Replace with your chat ID
CHATCTO_ID = "-1002351117426"  # Replace with your chat ID


bot = Bot(token=BOT_TOKEN) 



def get_chat_messages(chat_id):
    updates = []
    try:
        updates = asyncio.run(bot.getUpdates())
        print(updates)
        for update in updates:
            print(update)
    except Exception as e:
        return f"Error getting messages: {e}"
        
    #    if update.message and update.message.chat_id == chat_id:

    #        message_text = update.message.text

    #        print(f"Message from chat {chat_id}: {message_text}") 




    
def main():
    
    while True:
        time.sleep(2)
        print("Check")
        get_chat_messages(CHAT_ID)

    #asyncio.run(send_message_via_bot(BOT_TOKEN, CHAT_ID, crypto_statement))
    #time.sleep(1)
    #asyncio.run(send_message_via_bot(BOT_TOKEN, CHATCTO_ID, crypto_statement))
        

if __name__ == "__main__":
    main()
    
    
#7858647961:AAGTSFYjCBEhkUhNlpkBFAwNtCLynjQ2_W8
