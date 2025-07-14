# main.py

import asyncio
import os
from dotenv import load_dotenv
from telethon import TelegramClient
from url_identifier import identify_url_type

# Load secrets from .env
load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_username = os.getenv("BOT_USERNAME")

async def send_message_to_bot(text):
    async with TelegramClient('session_user', api_id, api_hash) as client:
        await client.send_message(bot_username, text)
        print(f"✅ Sent to bot: {text}")

if __name__ == "__main__":
    url = input("🔗 Enter URL: ").strip()
    url_type = identify_url_type(url)
    message = f"`{url_type}`\n"
    asyncio.run(send_message_to_bot(message))
