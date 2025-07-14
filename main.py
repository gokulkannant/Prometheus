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

# New flexible pattern to match progress
PROGRESS_REGEX = re.compile(
    r"(Download|Upload):\s(.+?)\n"                      # Group 1 = phase, Group 2 = filename
    r"\[.+?\]\s+(\d{1,3}\.\d+%)",                       # Group 3 = percent
    re.MULTILINE
)
ETA_REGEX = re.compile(r"ETA:\s*([^\s]+)", re.IGNORECASE)

def build_bar(percent: float, width: int = 24) -> str:
    done = int(width * percent / 100)
    bar = '█' * done + '░' * (width - done)
    return f"[{bar}]"

async def send_and_wait_for_cloud_link(command):
    async with TelegramClient('session_user', api_id, api_hash) as client:
        sent = await client.send_message(bot_username, command)
        sent_id = sent.id

        print("📤 Command sent. Waiting for progress and cloud link...\n")
        last_progress = ""

        while True:
            async for msg in client.iter_messages(bot_username, min_id=sent_id, reverse=False):
                # ✅ Check for cloud link
                if msg.buttons:
                    for row in msg.buttons:
                        for button in row:
                            if button.url:
                                #print(f"\n✅ Cloud Link: {button.url}")
                                return button.url

                # ✅ Match download/upload progress
                match = PROGRESS_REGEX.search(msg.text)
                if match:
                    phase = match.group(1)
                    filename = match.group(2)
                    percent_str = match.group(3).replace('%', '')

                    try:
                        percent_val = float(percent_str)
                    except ValueError:
                        continue

                    # Extract ETA from anywhere in the message
                    eta_match = ETA_REGEX.search(msg.text)
                    if eta_match:
                        eta = eta_match.group(1).strip()
                    else:
                        eta = "Unknown"

                    bar = build_bar(percent_val)
                    progress_line = (
                                        f"\n📦 {phase} Progress\n"
                                        f"📄 File: {filename}\n"
                                        f"{bar} {percent_val:.2f}% | ETA: {eta}"
                                                    )


                    if progress_line != last_progress:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(progress_line)
                        last_progress = progress_line
                #else:
                    # DEBUG: Print message to help improve the match
                    #if "Download" in msg.text or "Upload" in msg.text:
                        #print("⚠️ No regex match. Message content:\n", msg.text)

            await asyncio.sleep(1)

if __name__ == "__main__":
    url = input("🔗 Enter URL: ").strip()
    command = identify_url_type(url)
    link = asyncio.run(send_and_wait_for_cloud_link(command))

    if link:
        print(f"\n☁️ Final Cloud Link: {link}")
    else:
        print("\n❌ Cloud link not found.")
0