import os
import json
from datetime import datetime
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import MessageMediaPhoto
from pathlib import Path

# Load secrets from .env
load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")

# Directory setup
BASE_DIR = Path("data/raw")
MSG_DIR = BASE_DIR / "telegram_messages"
IMG_DIR = BASE_DIR / "telegram_images"
MSG_DIR.mkdir(parents=True, exist_ok=True)
IMG_DIR.mkdir(parents=True, exist_ok=True)

# Get today's date
today_str = datetime.today().strftime("%Y-%m-%d")

# Read channels from file
with open("channels.txt") as f:
    channels = [line.strip() for line in f if line.strip()]

def save_message_json(channel, messages):
    path = MSG_DIR / today_str
    path.mkdir(parents=True, exist_ok=True)
    outfile = path / f"{channel.replace('https://t.me/', '')}.json"
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

def download_images(message, channel):
    if not message.media or not isinstance(message.media, MessageMediaPhoto):
        return None

    img_folder = IMG_DIR / today_str / channel.replace("https://t.me/", "")
    img_folder.mkdir(parents=True, exist_ok=True)

    file_path = img_folder / f"{message.id}.jpg"
    return message.download_media(file=file_path)

with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
    for channel in channels:
        try:
            print(f"📥 Scraping from: {channel}")
            messages_data = []
            for message in client.iter_messages(channel, limit=100):
                # Save message text
                msg = {
                    "id": message.id,
                    "text": message.text,
                    "date": str(message.date),
                    "has_photo": bool(message.media),
                    "sender_id": message.sender_id
                }
                messages_data.append(msg)

                # Download photo if present
                if message.media:
                    download_images(message, channel)

            save_message_json(channel, messages_data)
            print(f"✅ Finished scraping {channel}")
        except Exception as e:
            print(f"❌ Error scraping {channel}: {e}")
