import asyncio
import logging
import requests
from flask import current_app
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from app.config.telegram import TELEGRAM_BOT_TOKEN
from app.services.user_service import update_user_chat_id

API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def send_telegram_otp(chat_id, otp):
    """Kirim pesan ke chat_id tertentu."""
    url = f"{API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": f"Ini kode otp: {otp}",
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        current_app.logger.error(f"Gagal mengirim pesan ke Telegram: {response.text}")
        return False
    return True


# Handler untuk perintah /start
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    username = update.effective_user.username

    if not username:
        await context.bot.send_message(chat_id=chat_id, text="Username Telegram tidak tersedia.")
        return

    await context.bot.send_message(chat_id=chat_id, text=f"Hai @{username}, kamu berhasil terhubung dengan bot.")
    update_user_chat_id(f"@{username}", chat_id)


# Fungsi menjalankan polling
def run_telegram_bot():
    asyncio.set_event_loop(asyncio.new_event_loop())
    app_bot = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start_handler))
    logging.basicConfig(level=logging.DEBUG)
    app_bot.run_polling()
