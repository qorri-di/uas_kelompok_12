import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ambil token dari .env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL_BASE")
WEBHOOK_PATH = os.getenv("WEBHOOK_URL_PATH")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN tidak ditemukan di file .env")

if not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL_BASE tidak ditemukan di file .env")

if not WEBHOOK_PATH:
    raise ValueError("WEBHOOK_URL_PATH tidak ditemukan di file .env")

# Format endpoint webhook Telegram
WEBHOOK_ENDPOINT = f"{WEBHOOK_URL}{WEBHOOK_PATH}"