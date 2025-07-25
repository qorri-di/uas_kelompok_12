from flask import Blueprint, request
from telegram import Update
from app.services.telegram_service import TELEGRAM_BOT_TOKEN
from telegram.ext import ApplicationBuilder

webhook_bp = Blueprint("webhook", __name__)


@webhook_bp.route("/webhook", methods=["POST"])
def telegram_webhook():
    if request.method == "POST":
        app_bot = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        update = Update.de_json(request.get_json(force=True), app_bot.bot)
        app_bot.update_queue.put_nowait(update)
        return "OK", 200
