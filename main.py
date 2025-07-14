from telethon import TelegramClient, events
import asyncio
import os
import re
from dotenv import load_dotenv
from url_identifier import identify_url_type

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_username = os.getenv("BOT_USERNAME")

# Regex pattern to extract link (http/https only)
URL_PATTERN = r'https?://\S+'

async def send_and_get_cloud_link(command):
    cloud_link = None

    async with TelegramClient('session_user', api_id, api_hash) as client:
        await client.send_message(bot_username, command)

        @client.on(events.NewMessage(from_users=bot_username))
        async def handler(event):
            nonlocal cloud_link
            if "Cloud Link" in event.raw_text:
                match = re.search(URL_PATTERN, event.raw_text)
                if match:
                    cloud_link = match.group(0)
                    print(f"☁️ Cloud Link: {cloud_link}")
                    await client.disconnect()

        print("⌛ Waiting for bot reply...")
        await client.run_until_disconnected()

    return cloud_link

if __name__ == "__main__":
    url = input("🔗 Enter URL: ").strip()
    command = identify_url_type(url)
    link = asyncio.run(send_and_get_cloud_link(command))
    if link:
        print(f"\n✅ Extracted Cloud Link: {link}")
    else:
        print("\n❌ Cloud link not found.")
