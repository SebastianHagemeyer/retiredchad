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

# Function to send a message via the Telegram bot
async def send_message_via_bot(token, chat_id, message):
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=message)


from telegram import Bot


# OPEN API KEY HERE

# Create a Bot instance
BOT_TOKEN = "8116421461:AAHXwr7YPiktp-wYvsWVbv7ZoPDvq8GtRTA"# os.environ["BOT_TOKEN"]
CHAT_ID = "-1002351117426"# Replace with your chat ID
CHATCTO_ID = "-1002351117426"  # Replace with your chat ID

#IDENTITY HERE
IDENTITY = "Your name is retired_chad_bot, You are a financial analyst in a group called retirement coin, youre really hype and cool and like participating in raiding social media posts. It's about retirement coin, generate a response, don't usehashtags, youre respoding in chat."
respondEX = r'\b(retired_chad_bot|chad)(?=\s|[.!?,]|$)'

bot = Bot(token=BOT_TOKEN) 

def extract_text_from_update(update):
    try:
        # Check if the update has a message and the message has text
        if hasattr(update, "message") and hasattr(update.message, "text"):
            return update.message.text
        else:
            return "No text in this message"
    except Exception as e:
        return f"Error extracting text: {e}"


offsetV = None
ogID = None
scanned = 0
currID = None

async def get_latest_offset():
    """Fetch only the latest update ID to start fresh."""
    try:
        async with bot:
            updates = await bot.getUpdates(offset=-1, limit=1, timeout=5)  # Get only the latest update
            
            if updates:
                latest_update_id = updates[-1].update_id
                print(f"Skipping past messages. Starting from update ID: {latest_update_id + 1}")
                return latest_update_id + 1  # Start from the next update
            else:
                return None  # No previous updates exist, so start normally
    except asyncio.TimeoutError:
        print("Request timed out.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None


async def fetch_updates():
    global ogID
    global scanned
    global offsetV
    updates = []

    try:
        async with bot:
            updates = await bot.getUpdates(offset=offsetV,limit=5)
        
            if updates:
                currID = updates[-1].update_id

                offsetV = currID + 1  

                if ogID is None:
                    ogID = currID
                scanned = currID - ogID

                print(scanned)  # Move offset forward)

                #offsetV = -1  # Move offset forward
    except asyncio.TimeoutError:
        print("Request timed out.")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return updates

messageID = 0
last_update_id = 0


def answer(question):
    """Respond as identity."""
    prompt = f"""
     {question}.
    
    """
    try:
        client = OpenAI(
            api_key = OPENAI_API_KEY,
        )

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "developer", "content": IDENTITY},
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        message = completion.choices[0].message 

        message_content = message.content
        print(message_content)
        return message_content
    
    except Exception as e:
        return f"Error generating statement: {e}"

async def get_chat_messages(chat_id):
    global messageID, last_update_id  # Declare global variables to modify them
    messagesA = []
    updates = []
    try:

        updates = await fetch_updates()

        for update in updates:
            
            said = extract_text_from_update(update)
            print(said)
            messagesA.append(said)

        
        last_update_id = messageID

        return messagesA

    except Exception as e:
        return f"Error getting messages: {e}"
        
    
async def main():
    global offsetV
    global respondEX

    offsetV = await get_latest_offset()

    while True:
        
        print("Check")
        messagesin = (await get_chat_messages(CHAT_ID))
        for m in messagesin:
            m = m.replace("'", r"\'")
            mlow = m.lower()
            if re.search(respondEX, mlow):
                print("asking",m)
                chadSays = answer(m)
                print("will say", chadSays)



                await asyncio.sleep(1)
                await send_message_via_bot(BOT_TOKEN, CHAT_ID, chadSays)

        print("Sleeping.")

        await asyncio.sleep(2) 
        

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Bot stopped.")