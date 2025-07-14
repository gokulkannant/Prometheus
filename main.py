from telethon import TelegramClient
import asyncio
import os
import re
from dotenv import load_dotenv
from url_identifier import identify_url_type

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_username = os.getenv("BOT_USERNAME")

async def send_and_get_cloud_link(command):
    async with TelegramClient('session_user', api_id, api_hash) as client:
        await client.send_message(bot_username, command)
        print("📨 Command sent. Waiting for bot reply with Cloud Link...")

        while True:
            async for msg in client.iter_messages(bot_username, limit=5):
                if "Cloud Link" in msg.text or msg.buttons:
                    if msg.buttons:
                        for row in msg.buttons:
                            for button in row:
                                if button.url:
                                    print(f"☁️ Cloud Link: {button.url}")
                                    return button.url
            await asyncio.sleep(5)

if __name__ == "__main__":
    url = input("🔗 Enter URL: ").strip()
    command = identify_url_type(url)
    link = asyncio.run(send_and_get_cloud_link(command))

    if link:
        print(f"\n✅ Final Result: {link}")
    else:
        print("\n❌ Cloud link not found.")
