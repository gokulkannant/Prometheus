from telethon import TelegramClient
import asyncio
import os
from dotenv import load_dotenv
from url_identifier import identify_url_type
import re

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_username = os.getenv("BOT_USERNAME")

PROGRESS_REGEX = re.compile(r"(Download|Upload): (.+?)\n\[.+?\]\s+(\d{1,3}\.\d+%)")

async def send_and_wait_for_cloud_link(command):
    async with TelegramClient('session_user', api_id, api_hash) as client:
        sent = await client.send_message(bot_username, command)
        sent_id = sent.id

        print("📤 Command sent. Waiting for progress updates and cloud link...\n")

        last_progress = ""

        while True:
            async for msg in client.iter_messages(bot_username, min_id=sent_id, reverse=False):
                # ✅ Check for cloud link in buttons
                if msg.buttons:
                    for row in msg.buttons:
                        for button in row:
                            if button.url:
                                print(f"\n✅ Cloud Link: {button.url}")
                                return button.url

                # ✅ Match progress (download or upload)
                match = PROGRESS_REGEX.search(msg.text)
                if match:
                    phase = match.group(1)  # Download or Upload
                    filename = match.group(2)
                    percent = match.group(3)

                    status = f"{phase}: {filename} — {percent}"
                    if status != last_progress:
                        print(f"📦 {status}")
                        last_progress = status

            await asyncio.sleep(2)

if __name__ == "__main__":
    url = input("🔗 Enter URL: ").strip()
    command = identify_url_type(url)
    link = asyncio.run(send_and_wait_for_cloud_link(command))

    if link:
        print(f"\n☁️ Final Cloud Link: {link}")
    else:
        print("\n❌ Cloud link not found.")
