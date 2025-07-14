from telethon import TelegramClient
import asyncio
import os
from dotenv import load_dotenv
from url_identifier import identify_url_type

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_username = os.getenv("BOT_USERNAME")

async def send_and_wait_for_cloud_link(command):
    async with TelegramClient('session_user', api_id, api_hash) as client:
        print("📨 Sending command to bot...")
        sent_msg = await client.send_message(bot_username, command)
        sent_id = sent_msg.id

        print("⏳ Waiting for cloud link to appear...")
        cloud_link = None

        while True:
            async for msg in client.iter_messages(bot_username, min_id=sent_id, reverse=False):
                # Only check new messages that have buttons
                if msg.buttons:
                    for row in msg.buttons:
                        for button in row:
                            if button.url:
                                cloud_link = button.url
                                print(f"✅ Cloud Link Found: {cloud_link}")
                                return cloud_link

            # Optional: print progress text to console
            async for msg in client.iter_messages(bot_username, min_id=sent_id, reverse=False):
                if "Download" in msg.text and not msg.buttons:
                    print("📦 Progress update:", msg.text.splitlines()[0])

            await asyncio.sleep(5)  # Wait before polling again

if __name__ == "__main__":
    url = input("🔗 Enter URL: ").strip()
    command = identify_url_type(url)
    link = asyncio.run(send_and_wait_for_cloud_link(command))

    if link:
        print(f"\n☁️ Final Cloud Link: {link}")
    else:
        print("\n❌ No link found.")
