import asyncio
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from app.config.telegram import TELEGRAM_BOT_TOKEN, WEBHOOK_ENDPOINT
from app.services.user_service import update_user_chat_id

app_bot = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()


# Fungsi kirim pesan OTP ke user
async def send_telegram_otp(chat_id: int, otp_code: str):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=chat_id, text=f"Kode OTP kamu adalah: {otp_code}")


# Handler untuk perintah /start
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    username = update.effective_user.username

    if not username:
        await context.bot.send_message(chat_id=chat_id, text="Username Telegram tidak tersedia.")
        return

    await context.bot.send_message(chat_id=chat_id, text=f"Hai @{username}, kamu berhasil terhubung dengan bot.")
    update_user_chat_id(username, chat_id)


# Fungsi menjalankan polling
def run_telegram_bot():
    app_bot.add_handler(CommandHandler("start", start_handler))

