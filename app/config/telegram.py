import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ambil token dari .env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN tidak ditemukan di file .env")

if not WEBHOOK_URL:
    raise ValueError("TELEGRAM_WEBHOOK_URL tidak ditemukan di file .env")

# Format endpoint webhook Telegram
WEBHOOK_ENDPOINT = f"{WEBHOOK_URL}/webhook"
